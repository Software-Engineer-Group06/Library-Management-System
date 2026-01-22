from models.db_connect import get_connection


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

    def create_issue_transaction(self, trans_id, member_id, book_id, due_date):
        """Tạo giao dịch mượn mới và cập nhật trạng thái sách thành 'Borrowed'"""
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
            cursor.execute(
                "UPDATE BorrowTransaction SET returnDate = NOW() WHERE transID = %s",
                (trans_id,),
            )
            
            # Cập nhật trạng thái sách về "Available"
            cursor.execute(
                "UPDATE Book SET status = %s WHERE bookID = %s",
                (self.STATUS_AVAILABLE, book_id),
            )
            
            # Nếu có tiền phạt, thêm record vào bảng Fine
            if fine_amount and fine_amount > 0:
                fine_id = f"FIN-{trans_id}"
                cursor.execute(
                    """
                    INSERT INTO Fine (fineID, transID, amount, isPaid) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (fine_id, trans_id, fine_amount, False),
                )
                
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