import pymysql
from datetime import datetime
from models.db_connect import get_connection

class ReportNotifyModel:
    def generate_notify_id(self):
        """Sinh ID: NOT-YYYY-XXX"""
        conn = get_connection()
        if not conn: 
            return None
        cursor = conn.cursor()
        
        prefix = f"NOT-{datetime.now().year}"
        try:
            cursor.execute("""
                SELECT notifyID 
                FROM Notification 
                WHERE notifyID LIKE %s 
                ORDER BY notifyID 
                DESC LIMIT 1""", (f"{prefix}-%",))
            result = cursor.fetchone()
            
            # Xử lý kết quả trả về (Tuple hoặc Dict)
            if result:
                val = result[0] if isinstance(result, tuple) else result['notifyID']
                last_seq = int(val.split('-')[-1])
                new_seq = last_seq + 1
            else:
                new_seq = 1
        except:
            new_seq = 1
        finally:
            cursor.close()
            conn.close()
            
        return f"{prefix}-{new_seq:03d}"

    def get_library_stats(self):
        """Thống kê tổng quan: Sách, Thành viên, Đang mượn, Quá hạn"""
        conn = get_connection()
        if not conn: 
            return None
        
        stats = {}
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Tổng đầu sách
            cursor.execute("SELECT COUNT(*) as total FROM Book")
            stats['books'] = cursor.fetchone()['total']
            
            # Tổng thành viên
            cursor.execute("SELECT COUNT(*) as total FROM Member")
            stats['members'] = cursor.fetchone()['total']
            
            # Đang mượn (Chưa trả)
            cursor.execute("SELECT COUNT(*) as total FROM BorrowTransaction WHERE returnDate IS NULL")
            stats['borrowing'] = cursor.fetchone()['total']
            
            # Sách quá hạn (Chưa trả + Quá hạn)
            cursor.execute("""
                SELECT COUNT(*) as total 
                FROM BorrowTransaction 
                WHERE returnDate IS NULL AND dueDate < NOW()
            """)
            stats['overdue'] = cursor.fetchone()['total']
            
        finally:
            conn.close()
        return stats

    def get_overdue_list(self):
        """Lấy danh sách chi tiết các phiếu mượn quá hạn"""
        conn = get_connection()
        if not conn: 
            return []
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """
                SELECT t.transID, m.memberID, u.fullName, b.title, t.dueDate 
                FROM BorrowTransaction t
                JOIN Member m ON t.memberID = m.memberID
                JOIN User u ON m.userID = u.userID
                JOIN Book b ON t.bookID = b.bookID
                WHERE t.returnDate IS NULL AND t.dueDate < NOW()
            """
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            conn.close()

    def send_notification(self, member_id, message):
        """Gửi thông báo cho thành viên"""
        conn = get_connection()
        if not conn: 
            return False
        try:
            cursor = conn.cursor()
            notify_id = self.generate_notify_id()
            
            cursor.execute("""
                INSERT INTO Notification (notifyID, memberID, message, sentDate, isRead)
                VALUES (%s, %s, %s, NOW(), 0)
            """, (notify_id, member_id, message))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error sending notify: {e}")
            return False
        finally:
            conn.close()