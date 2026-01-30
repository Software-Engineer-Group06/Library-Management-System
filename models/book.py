from models.db_connect import get_connection

class BookModel:
    def __init__(self):
        self.db = get_connection()

    def search_books(self, keyword):
        """
        Search Logic: The search result shall support partial matching 
        (Title, Author, ISBN, or Category).
        """
        cursor = self.db.cursor(dictionary=True)
        # Sử dụng LIKE %...% để tìm kiếm gần đúng
        query = """
            SELECT * FROM BOOK 
            WHERE title LIKE %s 
            OR author LIKE %s 
            OR ISBN LIKE %s 
            OR category LIKE %s
        """
        param = f"%{keyword}%"
        cursor.execute(query, (param, param, param, param))
        return cursor.fetchall()

    def add_book(self, book_data):
        try:
            cursor = self.db.cursor()
            query = """
                INSERT INTO BOOK (bookID, title, author, ISBN, publisher, category, shelfLocation, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Available')
            """
            cursor.execute(query, (
                book_data['bookID'], book_data['title'], book_data['author'],
                book_data['ISBN'], book_data['publisher'], 
                book_data['category'], book_data['shelfLocation']
            ))
            self.db.commit()
            return True
        except Exception as e:
            print(f"\n❌ [DEBUG ERROR] Chi tiết lỗi SQL: {e}")
            self.db.rollback()
            return False

    def update_book(self, book_id, update_data):
        try:
            cursor = self.db.cursor()
            # Ví dụ cập nhật Title và Author (thực tế có thể cần cập nhật nhiều field hơn)
            query = "UPDATE BOOK SET title = %s, author = %s WHERE bookID = %s"
            cursor.execute(query, (update_data['title'], update_data['author'], book_id))
            self.db.commit()
            return True
        except Exception:
            return False

    def delete_book(self, book_id):
        try:
            cursor = self.db.cursor()
            query = "DELETE FROM BOOK WHERE bookID = %s"
            cursor.execute(query, (book_id,))
            self.db.commit()
            return True
        except Exception:
            return False

    def get_book_by_id(self, book_id):
        cursor = self.db.cursor(dictionary=True)
        query = "SELECT * FROM BOOK WHERE bookID = %s"
        cursor.execute(query, (book_id,))
        return cursor.fetchone()