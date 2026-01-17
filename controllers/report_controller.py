from models.db_connect import Database

class ReportService:
    def __init__(self):
        self.db = Database()

    def overdue_books_report(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT b.title, m.full_name, br.due_date,
               DATEDIFF(CURDATE(), br.due_date) AS overdue_days
        FROM borrowings br
        JOIN books b ON br.book_id = b.book_id
        JOIN members m ON br.member_id = m.member_id
        WHERE br.return_date IS NULL
        AND br.due_date < CURDATE()
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        self.db.close()
        return result

    def most_borrowed_books_report(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        query = """
        SELECT b.title, COUNT(*) AS times
        FROM borrowings br
        JOIN books b ON br.book_id = b.book_id
        GROUP BY br.book_id
        ORDER BY times DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        self.db.close()
        return result

    def total_fines_report(self):
        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM fines WHERE status='PAID'")
        total = cursor.fetchone()[0] or 0

        cursor.close()
        self.db.close()
        return total