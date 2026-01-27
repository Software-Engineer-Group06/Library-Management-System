from datetime import datetime, timedelta
import uuid
from models.db_connect import get_connection

class CirculationModel:
    def __init__(self):
        self.db = get_connection()

    def check_eligibility(self, member_id):
        """
        Kiểm tra điều kiện mượn:
        1. Số sách đang mượn < BorrowLimit
        2. Không có nợ phạt > 50,000 VND 
        """
        cursor = self.db.cursor(dictionary=True)
        
        # Lấy thông tin user để biết Limit
        cursor.execute("SELECT role FROM USER WHERE userID = %s", (member_id,))
        user = cursor.fetchone()
        if not user: return False, "Member not found"
        
        # Limit: Student(2) -> 5, Teacher -> 10
        limit = 5 if user['role'] == 2 else 10 
        
        # Đếm sách đang mượn (ReturnDate IS NULL)
        cursor.execute("""
            SELECT COUNT(*) as count FROM BORROW_TRANSACTION 
            WHERE memberID = %s AND ReturnDate IS NULL
        """, (member_id,))
        borrowed_count = cursor.fetchone()['count']
        
        if borrowed_count >= limit:
            return False, "Borrowing limit exceeded"

        # 2. Kiểm tra tổng tiền phạt chưa đóng
        cursor.execute("""
            SELECT SUM(Amount) as total_fine FROM FINE 
            JOIN BORROW_TRANSACTION ON FINE.TransID = BORROW_TRANSACTION.TransID
            WHERE memberID = %s AND Paid = FALSE
        """, (member_id,))
        result = cursor.fetchone()
        total_fine = result['total_fine'] if result['total_fine'] else 0.0
        
        if total_fine > 50000:
            return False, "Unpaid fines greater than 50,000 VND"
            
        return True, "Eligible"

    def issue_book(self, member_id, book_id, due_date):
        """
        Thực hiện mượn sách với ACID Transaction
        """
        try:
            # Bắt đầu transaction
            self.db.start_transaction()
            cursor = self.db.cursor()

            # Kiểm tra sách có Available không
            cursor.execute("SELECT status FROM BOOK WHERE bookID = %s", (book_id,))
            book = cursor.fetchone()
            if not book or book[0] != 'Available':
                self.db.rollback()
                return False, "Book unavailable"

            # Insert Transaction Record
            trans_id = str(uuid.uuid4())[:8] # Generate short ID
            issue_date = datetime.now().strftime('%Y-%m-%d')
            
            query_trans = """
                INSERT INTO BORROW_TRANSACTION (TransID, IssueDate, DueDate, memberID, bookID)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_trans, (trans_id, issue_date, due_date, member_id, book_id))

            # Update Book Status -> Issued
            cursor.execute("UPDATE BOOK SET status = 'Issued' WHERE bookID = %s", (book_id,))

            # Commit nếu cả 2 thành công
            self.db.commit()
            return True, "Success"
        except Exception as e:
            self.db.rollback() # Rollback nếu lỗi
            return False, str(e)

    def return_book(self, book_id):
        try:
            self.db.start_transaction()
            cursor = self.db.cursor(dictionary=True)

            # Tìm giao dịch mượn đang mở (ReturnDate is NULL)
            cursor.execute("""
                SELECT * FROM BORROW_TRANSACTION 
                WHERE bookID = %s AND ReturnDate IS NULL
            """, (book_id,))
            trans = cursor.fetchone()
            
            if not trans:
                self.db.rollback()
                return None # Không tìm thấy giao dịch

            # Update ReturnDate là Current Date
            return_date = datetime.now().date()
            cursor.execute("""
                UPDATE BORROW_TRANSACTION SET ReturnDate = %s 
                WHERE TransID = %s
            """, (return_date, trans['TransID']))

            # Update Book Status -> Available
            cursor.execute("UPDATE BOOK SET status = 'Available' WHERE bookID = %s", (book_id,))

            # Tính phạt 
            due_date = trans['DueDate'] # Date object from DB
            # Ép kiểu date nếu cần
            if isinstance(due_date, str):
                due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                
            overdue_days = (return_date - due_date).days
            fine_amount = 0
            
            if overdue_days > 0:
                fine_amount = overdue_days * 5000
                # Lưu vào bảng FINE
                fine_id = str(uuid.uuid4())[:8]
                cursor.execute("""
                    INSERT INTO FINE (FineID, Amount, TransID) VALUES (%s, %s, %s)
                """, (fine_id, fine_amount, trans['TransID']))

            self.db.commit()
            
            return {
                'late_days': max(0, overdue_days),
                'fine_amount': fine_amount
            }
            
        except Exception as e:
            print(e)
            self.db.rollback()
            return None
    def get_borrowing_history(self, member_id):
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT BT.TransID, B.Title, BT.IssueDate, BT.DueDate, BT.ReturnDate
            FROM BORROW_TRANSACTION BT
            JOIN BOOK B ON BT.bookID = B.bookID
            WHERE BT.memberID = %s
        """
        cursor.execute(query, (member_id,))
        return cursor.fetchall()

    def reserve_book(self, member_id, book_id):
        try:
            self.db.start_transaction()
            cursor = self.db.cursor(dictionary=True)

            # Kiểm tra trạng thái sách 
            # Nếu sách đang 'Available' hoặc 'Lost' thì từ chối.
            cursor.execute("SELECT status FROM BOOK WHERE bookID = %s", (book_id,))
            book = cursor.fetchone()
            
            if not book:
                self.db.rollback()
                return False, "Book ID not found."
            
            if book['status'] == 'Available':
                self.db.rollback()
                return False, "Book is currently Available. Please borrow it directly instead of reserving."
            
            if book['status'] == 'Lost':
                self.db.rollback()
                return False, "Book is Lost and cannot be reserved."

            # Kiểm tra xem user đã đặt trước cuốn này chưa (tránh spam)
            check_query = """
                SELECT COUNT(*) as count FROM RESERVATION 
                WHERE memberID = %s AND bookID = %s AND Status = 'Active'
            """
            cursor.execute(check_query, (member_id, book_id))
            if cursor.fetchone()['count'] > 0:
                self.db.rollback()
                return False, "You already have an active reservation for this book."

            # Tạo bản ghi đặt trước (Insert Reservation)
            res_id = str(uuid.uuid4())[:8]
            res_date = datetime.now().strftime('%Y-%m-%d')
            
            insert_query = """
                INSERT INTO RESERVATION (ReservationID, Status, ReservationDate, memberID, bookID)
                VALUES (%s, %s, %s, %s, %s)
            """
            # Status mặc định là 'Active' để chờ sách trả về
            cursor.execute(insert_query, (res_id, 'Active', res_date, member_id, book_id))

            self.db.commit()
            return True, "Reservation successful. You will be notified when the book is available."

        except Exception as e:
            self.db.rollback()
            print(f"[Error] Reserve Book: {e}")
            return False, "System error during reservation."
    def get_fine_details(self, trans_id):
        """
        Lấy thông tin tiền phạt dựa trên Transaction ID
        """
        cursor = self.db.cursor(dictionary=True)
        # Join bảng FINE và BORROW_TRANSACTION để lấy ngày và trạng thái
        query = """
            SELECT F.FineID, F.Amount, F.Paid, BT.TransID, BT.DueDate, BT.ReturnDate
            FROM FINE F
            JOIN BORROW_TRANSACTION BT ON F.TransID = BT.TransID
            WHERE BT.TransID = %s
        """
        cursor.execute(query, (trans_id,))
        result = cursor.fetchone()
        
        if result:
            # Tính số ngày trễ để hiển thị
            if result['ReturnDate'] and result['DueDate']:
                # Ép kiểu nếu driver trả về string
                r_date = result['ReturnDate']
                d_date = result['DueDate']
                # Nếu là string thì convert, nếu là date thì trừ trực tiếp
                from datetime import datetime, date
                if isinstance(r_date, str): r_date = datetime.strptime(r_date, '%Y-%m-%d').date()
                if isinstance(d_date, str): d_date = datetime.strptime(d_date, '%Y-%m-%d').date()
                
                late_days = (r_date - d_date).days
                result['late_days'] = max(0, late_days)
            else:
                result['late_days'] = 0
                
            return result
        return None

    def pay_fine(self, fine_id):
        """
        Thanh toán tiền phạt
        """
        try:
            cursor = self.db.cursor()
            query = "UPDATE FINE SET Paid = TRUE WHERE FineID = %s"
            cursor.execute(query, (fine_id,))
            self.db.commit()
            return True
        except Exception:
            return False