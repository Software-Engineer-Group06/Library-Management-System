from datetime import datetime, timedelta
import uuid
from models.db_connect import get_connection

class ReportModel:
    def __init__(self):
        self.db = get_connection()

    def get_overdue_books(self):
        """
        List of Overdue Books 
        Logic: ReturnDate IS NULL và DueDate < Current Date
        """
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT B.bookID, B.Title, BT.DueDate, U.fullName
            FROM BORROW_TRANSACTION BT
            JOIN BOOK B ON BT.bookID = B.bookID
            JOIN USER U ON BT.memberID = U.userID
            WHERE BT.ReturnDate IS NULL AND BT.DueDate < CURDATE()
        """
        cursor.execute(query)
        return cursor.fetchall()

    def get_most_borrowed_books(self):
        """
        Most Borrowed Books 
        Logic: Count số lần xuất hiện trong bảng Transaction
        """
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT B.Title, COUNT(BT.bookID) as borrow_count
            FROM BORROW_TRANSACTION BT
            JOIN BOOK B ON BT.bookID = B.bookID
            GROUP BY B.Title
            ORDER BY borrow_count DESC
            LIMIT 10
        """
        cursor.execute(query)
        return cursor.fetchall()

    def get_total_fines_collected(self):
        """
        Total Fines Collected 
        Logic: Tổng tiền các biên lai phạt đã thanh toán (Paid = 1)
        """
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT SUM(Amount) as total FROM FINE WHERE Paid = 1"
        cursor.execute(query)
        result = cursor.fetchone()
        return result['total'] if result['total'] else 0.0

    def get_member_notifications(self, member_id):
        """Lấy danh sách thông báo của 1 member"""
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM NOTIFICATION WHERE memberID = %s ORDER BY SentDate DESC"
        cursor.execute(query, (member_id,))
        return cursor.fetchall()

    def generate_due_date_reminders(self):
        """
        Tự động tạo thông báo nhắc nhở trước 2 ngày
        Chạy mỗi khi hệ thống khởi động hoặc admin login.
        """
        cursor = self.db.cursor(dictionary=True)
        # Tìm các giao dịch có DueDate là ngày kia (Today + 2 days)
        target_date = (datetime.now() + timedelta(days=2)).date()
        
        query = """
            SELECT memberID, bookID FROM BORROW_TRANSACTION 
            WHERE DueDate = %s AND ReturnDate IS NULL
        """
        cursor.execute(query, (target_date,))
        upcoming_dues = cursor.fetchall()
        
        for record in upcoming_dues:
            # Tạo thông báo mới
            notif_id = str(uuid.uuid4())[:8]
            sent_date = datetime.now().strftime('%Y-%m-%d')
            msg = f"Reminder: Book (ID: {record['bookID']}) is due in 2 days."
            
            # Kiểm tra tránh trùng lặp nếu cần, ở đây insert luôn
            insert_query = "INSERT INTO NOTIFICATION VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (notif_id, sent_date, msg, record['memberID']))
        
        self.db.commit()