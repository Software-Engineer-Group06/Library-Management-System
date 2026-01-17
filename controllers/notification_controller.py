from models.db_connect import Database

class NotificationService:
    def __init__(self):
        self.db = Database()

    def due_soon_notifications(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT member_id, book_id
        FROM borrowings
        WHERE return_date IS NULL
        AND DATEDIFF(due_date, CURDATE()) = 2
        """

        cursor.execute(query)

        for row in cursor.fetchall():
            msg = f"Reminder: Book {row['book_id']} is due in 2 days."
            cursor.execute(
                "INSERT INTO notifications (member_id, message) VALUES (%s, %s)",
                (row["member_id"], msg)
            )

        conn.commit()
        cursor.close()
        self.db.close()

    # MEMBER
    def get_notifications(self, member_id):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT message, created_at FROM notifications WHERE member_id=%s",
            (member_id,)
        )

        data = cursor.fetchall()
        cursor.close()
        self.db.close()
        return data

    def show_notifications(member_id):
        service = NotificationService()
        data = service.get_notifications(member_id)

        if not data:
            print("No notifications.")
        else:
            for msg, time in data:
                print(f"[{time}] {msg}")