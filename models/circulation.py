from models.db_connect import get_connection
from datetime import datetime

class CirculationModel:
    STATUS_ISSUED = "Issued"
    STATUS_AVAILABLE = "Available"
    
    def __init__(self):
        pass
    
    def get_member_stats(self, member_id):
        """Truy vấn DB để lấy số lượng sách chưa trả và tổng tiền phạt chưa thanh toán"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # thêm ngoại lệ nếu không tìm thấy member id
        try:
            # Đếm số giao dịch chưa trả (returnDate IS NULL)
            cursor.execute(
                """
                SELECT COUNT(*) FROM BorrowTransaction 
                WHERE memberID = %s AND returnDate IS NULL
                """,
                (member_id,),
            )
            borrowed_count = cursor.fetchone()[0]
            
            # Tính tổng tiền phạt chưa thanh toán (isPaid = False) từ bảng Fine
            cursor.execute(
                """
                SELECT SUM(f.amount) 
                FROM Fine f
                JOIN BorrowTransaction br ON f.transID = br.transID
                WHERE br.memberID = %s AND f.isPaid = False
                """,
                (member_id,),
            )
            total_fines = cursor.fetchone()[0] or 0
            
            return borrowed_count, total_fines
        
        except Exception as e:
            conn.rollback() 
            print(f"System error: {e}")
            return None, None
            
        finally:
            cursor.close()
            conn.close()

    def check_book_status(self, book_id):
        """Kiểm tra tình trạng sách hiện tại"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT status FROM Book WHERE bookID = %s", (book_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None  # Không tìm thấy
        finally:
            cursor.close()
            conn.close()
            
    def get_member_type(self, member_id):
        """Lấy vai trò của member (Student/Teacher) từ database"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT memberType FROM Member WHERE memberID = %s", (member_id,))
            result = cursor.fetchone()
            
            if result:
                return result[0]  # Trả về 'Student' hoặc 'Teacher'
            return None  # Không tìm thấy thành viên
        except Exception as e:
            print(f"Model Error: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_due_date(self, book_id):
        """Lấy ngày đến hạn (dueDate) của một cuốn sách đang được mượn"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Truy vấn bản ghi mượn sách mới nhất mà chưa có ngày trả (returnDate IS NULL)
            cursor.execute("""
                SELECT dueDate FROM BorrowTransaction 
                WHERE bookID = %s AND returnDate IS NULL
                ORDER BY transID DESC LIMIT 1
                """, 
                (book_id,)
            )
            result = cursor.fetchone()
            
            # Trả về đối tượng date nếu tìm thấy, ngược lại trả về None
            return result[0] if result else None
            
        except Exception as e:
            print(f"Model Error (get_due_date): {e}")
            return None
        finally:
            cursor.close()
            conn.close()
        
        
    def create_issue_transaction(self, trans_id, member_id, book_id, due_date):
        """Tạo giao dịch mượn mới và cập nhật trạng thái sách thành 'Issued'"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # thêm xử lý ngoại lệ nhằm trường hợp insert hoặc update không hoạt động ảnh hưởng đến db
        try:
            # Cố gắng đặt trạng thái sách là Issued chỉ khi đang Available
            cursor.execute(
                "UPDATE Book SET status = %s WHERE bookID = %s AND status = %s",
                (self.STATUS_ISSUED, book_id, self.STATUS_AVAILABLE),
            )
            if cursor.rowcount == 0:
                # Không thể cập nhật: sách không còn Available
                conn.rollback()
                return False
            
            # Thêm bản ghi vào bảng BorrowTransaction
            cursor.execute(
                """
                INSERT INTO BorrowTransaction (transID, memberID, bookID, dueDate)
                VALUES (%s, %s, %s, %s)
                """,
                (trans_id, member_id, book_id, due_date),
            )
            
            conn.commit()
            return True
        
        except Exception as e:
            conn.rollback() 
            print(f"System error: {e}")
            return False
            
        finally:
            cursor.close()
            conn.close()
    def issue_book(self, member_id, book_id):
        """
        Hàm xử lý trọn gói quy trình mượn sách.
        Logic: Check sách -> Check hạn mức -> Sinh ID -> Tính ngày trả -> Insert DB
        Output: Chuỗi thông báo kết quả (SUCCESS|... hoặc LIMIT_EXCEEDED|...)
        """
        conn = get_connection()
        if not conn: return "DB_ERROR"
        
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            # B1: Kiểm tra sách có sẵn sàng không
            cursor.execute("SELECT status, title FROM Book WHERE bookID = %s", (book_id,))
            book = cursor.fetchone()
            if not book: return "BOOK_NOT_FOUND"
            if book['status'] != self.STATUS_AVAILABLE: return "BOOK_NOT_AVAILABLE"

            # B2: Kiểm tra hạn mức mượn (Sinh viên max 5, GV max 10)
            # Lấy role
            cursor.execute("SELECT memberType, borrowLimit FROM Member WHERE memberID = %s", (member_id,))
            member = cursor.fetchone()
            if not member: return "MEMBER_NOT_FOUND"

            # Đếm số sách đang mượn
            cursor.execute("SELECT COUNT(*) as count FROM BorrowTransaction WHERE memberID = %s AND returnDate IS NULL", (member_id,))
            current_borrow = cursor.fetchone()['count']
            
            # Logic check limit (Ưu tiên số trong DB, nếu null thì mặc định 5)
            limit = member['borrowLimit'] if member['borrowLimit'] else 5
            if current_borrow >= limit:
                return "LIMIT_EXCEEDED"

            # B3: Chuẩn bị dữ liệu Insert
            trans_id = self.create_transID() # Gọi hàm sinh ID nội bộ
            # Mượn 14 ngày
            due_date = datetime.now() + timedelta(days=14)

            # B4: Thực hiện Transaction (Gọi hàm Insert cấp thấp)
            if self.create_issue_transaction(trans_id, member_id, book_id, due_date):
                return f"SUCCESS|{trans_id}|{book['title']}|{due_date.date()}"
            else:
                return "INSERT_FAILED"

        except Exception as e:
            print(f"Error issue_book: {e}")
            return f"SYSTEM_ERROR|{e}"
        finally:
            conn.close()
        

    def update_return_book(self, book_id, fine_amount):
        """Cập nhật ngày trả, trạng thái sách và tạo phiếu phạt nếu có"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # thêm xử lý ngoại lệ khi update borrowtrans hoặc update book bị lỗi ảnh hưởng đến database
        try:
            # Tìm giao dịch theo book_id
            cursor.execute(
                """
                SELECT transID FROM BorrowTransaction
                WHERE bookID = %s AND returnDate IS NULL
                """,
                (book_id,),
            )
            result = cursor.fetchone()
            
            if result is None:
                print("This Borrow transaction could not be found.")
                return False
            
            trans_id = result[0] # Lấy giá trị transID từ tuple kết quả
            
            # Cập nhật ngày trả sách trong BorrowTransaction
            cursor.execute("""
                UPDATE BorrowTransaction 
                SET returnDate = NOW() WHERE transID = %s
            """,(trans_id,),)
            
            # Cập nhật trạng thái sách về "Available"
            cursor.execute("""
                UPDATE Book 
                SET status = %s WHERE bookID = %s
            """,(self.STATUS_AVAILABLE, book_id),)
            
            # Nếu có tiền phạt, thêm record vào bảng Fine
            if fine_amount and fine_amount > 0:
                fine_id = f"F-{trans_id}"
                cursor.execute(
                    """
                    INSERT INTO Fine (fineID, transID, amount, isPaid) 
                    VALUES (%s, %s, %s, %s)
                    """,(fine_id, trans_id, fine_amount, False),)
                
            conn.commit()
            print(f"Book returned successfully! Transaction code {trans_id}")
            
            return True
        
        except Exception as e:
            conn.rollback()     # Nếu có lỗi thì các update sẽ được đặt lại không thay đổi db
            print(f"System error: {e}")
            return False
            
        finally:
            cursor.close()
            conn.close()
            
    def get_fine_details(self, trans_id):
        """Lấy chi tiết tiền phạt dựa trên mã giao dịch"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Truy vấn kết hợp bảng Fine và BorrowTransaction để tính số ngày trễ
            cursor.execute(
            """
                SELECT f.transID, f.amount, f.isPaid, DATEDIFF(br.returnDate, br.dueDate) as lateDays
                FROM Fine f
                JOIN BorrowTransaction br ON f.transID = br.transID
                WHERE f.transID = %s
            """,
            (trans_id,),
            )
            return cursor.fetchone() # Trả về tuple hoặc None
        finally:
            cursor.close()
            conn.close()

    def update_fine_payment(self, trans_id):
        """Cập nhật trạng thái đã thanh toán tiền phạt"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE Fine SET isPaid = TRUE WHERE transID = %s", (trans_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Error updating payment: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    def create_transID(self):
        """Tạo mã giao dịch tự tăng theo định dạng T-YYYY-XXXX"""
        conn = get_connection()
        cursor = conn.cursor()
        
        current_year = datetime.now().year
        prefix = f"T-{current_year}"
        
        try:
            # Tìm mã giao dịch lớn nhất của năm hiện tại
            cursor.execute("""
                SELECT transID 
                FROM BorrowTransaction 
                WHERE transID LIKE %s 
                ORDER BY transID DESC LIMIT 1
            """, (f"{prefix}-%",))
            
            result = cursor.fetchone()
            
            if result:
                # result[0] ví dụ: "T-2026-0005" -> tách lấy "0005" -> chuyển thành 5
                last_val = result[0]
                last_seq = int(last_val.split('-')[-1])
                new_seq = last_seq + 1
            else:
                # Nếu năm mới chưa có giao dịch nào
                new_seq = 1
                
            return f"{prefix}-{new_seq:04d}" # Trả về định dạng T-2026-0001
            
        except Exception as e:
            print(f"Error creating transID: {e}")
            return f"T-{datetime.now().strftime('%Y%m%d%H%M%S')}" # Fallback nếu lỗi
        finally:
            cursor.close()
            conn.close()