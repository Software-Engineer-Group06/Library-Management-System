from datetime import datetime
import pymysql
from models.db_connect import get_connection

class BookModel:
    def generate_book_id(self):
        """Sinh ID tự động: BK-YYYY-XXX (Ví dụ: BK-2026-001)"""
        conn = get_connection()
        if not conn: return None
        cursor = conn.cursor()
        
        current_year = datetime.now().year
        prefix = f"BK-{current_year}"
        
        try:
            # Lấy mã sách cuối cùng trong năm nay
            cursor.execute("""
                SELECT bookID 
                FROM Book 
                WHERE bookID LIKE %s 
                ORDER BY bookID 
                DESC LIMIT 1""", (f"{prefix}-%",))
            result = cursor.fetchone()
            
            if result:
                # result là dict {'bookID': 'BK-2026-005'}
                val = result[0] if isinstance(result, tuple) else result['bookID']
                last_seq = int(val.split('-')[-1])
                new_seq = last_seq + 1
            else:
                new_seq = 1
        except Exception as e:
            print(f"Error gen ID: {e}")
            new_seq = 1
        finally:
            cursor.close()
            conn.close()
            
        return f"{prefix}-{new_seq:03d}"

    def add_book(self, title, author, isbn, publisher, category, shelf):
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            new_id = self.generate_book_id()
            
            cursor.execute("""
                INSERT INTO Book (bookID, title, author, isbn, publisher, category, shelfLocation, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Available')
            """, (new_id, title, author, isbn, publisher, category, shelf))
            conn.commit()
            return new_id
        except Exception as e:
            print(f"Error adding book: {e}")
            return None
        finally:
            conn.close()

    def search_books(self, keyword):
        """Tìm sách theo Tên, Tác giả hoặc Category"""
        conn = get_connection()
        if not conn: 
            return []
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # Thêm dấu % để tìm kiếm gần đúng (Partial Match)
            search_term = f"%{keyword}%"
            cursor.execute("""
                SELECT * FROM Book 
                WHERE title LIKE %s OR author LIKE %s OR category LIKE %s OR bookID LIKE %s
            """, (search_term, search_term, search_term, search_term))
            return cursor.fetchall()
        finally:
            conn.close()

    def delete_book(self, book_id):
        conn = get_connection()
        if not conn: 
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Book WHERE bookID = %s", (book_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False
        finally:
            conn.close()