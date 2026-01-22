import mysql
import mysql.connector

from models.db_connect import Database

class NotificationService:
    def __init__(self):
        self.db = Database()

    def show_notifications(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT message, sentDate 
        FROM Notification 
        ORDER BY sentDate DESC
        """
    
        try:
            cursor.execute(query)
            notifications = cursor.fetchall()

            if not notifications:
                print("\nNo notifications:")
                print("No new notifications.")
                return

            print("\nNotifications exist:")
            print("\nNotifications:")
        
            for note in notifications:
                formatted_date = note['sentDate'].strftime("%d/%m/%Y")
                print(f"[{formatted_date}] {note['message']}")

        except Exception as err:
            print(f"Lỗi khi tải thông báo: {err}")
        finally:
            cursor.close()
            conn.close()
    def generate_due_reminders(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
    
        # Tìm các sách còn đúng 2 ngày nữa là đến hạn (DATEDIFF = 2)
        # và chưa trả (returnDate IS NULL)
        query_check = """
        SELECT bt.memberID, b.title, bt.dueDate
        FROM BorrowTransaction bt
        JOIN Book b ON bt.bookID = b.bookID
        WHERE bt.returnDate IS NULL 
          AND DATEDIFF(bt.dueDate, CURDATE()) = 2
        """
    
        try:
            cursor.execute(query_check)
            due_soon = cursor.fetchall()
        
            for record in due_soon:
                msg = f"Reminder: Book '{record['title']}' is due in 2 days."
            
                # Chèn vào bảng Notification (ID tự sinh hoặc bạn tự định nghĩa)
                # Giả sử dùng hàm tạo ID đơn giản
                notify_id = f"NOTI{datetime.now().strftime('%f')}" 
            
                insert_query = """
                INSERT INTO Notification (notifyID, memberID, message, sentDate)
                VALUES (%s, %s, %s, NOW())
                """
                cursor.execute(insert_query, (notify_id, record['memberID'], msg))
        
            conn.commit()
        except Exception as err:
            print(f"Lỗi tạo nhắc nhở: {err}")
        finally:
            cursor.close()
            conn.close()
