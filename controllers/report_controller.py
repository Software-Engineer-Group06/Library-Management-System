import mysql
import mysql.connector

from models.db_connect import Database
from datetime import datetime
class ReportService:
    def __init__(self):
        self.db = Database()

    def get_overdue_books(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        query = """
    SELECT 
        bt.transID,
        m.memberID,
        u.fullName AS memberName,
        b.title AS bookTitle,
        bt.issueDate,
        bt.dueDate
    FROM BorrowTransaction bt
    JOIN Member m ON bt.memberID = m.memberID
    JOIN User u ON m.userID = u.userID
    JOIN Book b ON bt.bookID = b.bookID
    WHERE bt.returnDate IS NULL 
      AND bt.dueDate < %s
    """
        try: 
            current_time = datetime.now()
            cursor.execute(query, (current_time,))
            overdue_list = cursor.fetchall()
            if not overdue_list:
                print("--- There are no overdue books! ---")
                return []
            
            for row in overdue_list:
                delta = current_time - row['dueDate']
                days_overdue = delta.days
                print(f"{row['bookID']:<10} | {row['memberID']:<12} | {row['memberName']:<20} | {days_overdue:<12} | {row['bookTitle']}")
            return overdue_list
        except mysql.connector.Error as err:    
            print(f"Query Failed: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def get_most_borrowed_books_report(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        query = """
    SELECT 
        b.bookID,
        b.title,
        b.author,
        b.category,
        COUNT(bt.transID) AS borrow_count
    FROM Book b
    LEFT JOIN BorrowTransaction bt ON b.bookID = bt.bookID
    GROUP BY b.bookID, b.title, b.author, b.category
    HAVING borrow_count > 0
    ORDER BY borrow_count DESC
    LIMIT %s
    """
        try:
            cursor.execute(query,(5,))
            result = cursor.fetchall()
            if not result:
                print("There are no data!")
                return []
            print(f"\n--- TOP {5} MOST BORROWED BOOK ---")
            print(f"{'Rank':<5} | {'Book ID':<10} | {'Borrow Count':<12} | {'Title'}")
            print("-" * 70)
        
            for i, row in enumerate(result, 1):
                print(f"{i:<5} | {row['bookID']:<10} | {row['borrow_count']:<12} | {row['title']}")
            
            return result
        except Exception as err:
            print(f"Query Failed: {err}")
            return []
        finally:
            cursor.close()
            conn.close()


    def show_all_overdue_fines(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
    
        
        query = """
        SELECT 
            bt.transID,
            u.fullName,
            bt.dueDate,
            b.title AS bookTitle
        FROM BorrowTransaction bt
        JOIN Member m ON bt.memberID = m.memberID
        JOIN User u ON m.userID = u.userID
        JOIN Book b ON bt.bookID = b.bookID
        WHERE bt.returnDate IS NULL 
          AND bt.dueDate < %s
        """
    
        try:
            current_time = datetime.now()
            cursor.execute(query, (current_time,))
            overdue_records = cursor.fetchall()
        
            if not overdue_records:
                print("\n--- No one returned the books late. ---")
                return

            print(f"\n{'='*85}")
            print(f"{'ID':<7} | {'Người mượn':<20} | {'Ngày hạn':<12} | {'Trễ (Ngày)':<10} | {'Tiền phạt (VND)'}")
            print(f"{'-'*85}")

            total_fine = 0
            fine_per_day = 5000  

            for row in overdue_records:
                # Tính số ngày trễ
                delta = current_time - row['dueDate']
                days_overdue = delta.days
            
                # Tính tiền phạt
                amount = days_overdue * fine_per_day
                total_fine += amount
            
                print(f"{row['transID']:<7} | {row['fullName']:<20} | {row['dueDate'].strftime('%Y-%m-%d')} | {days_overdue:<10} | {amount:,.0f}")

            print(f"{'-'*85}")
            print(f"Tổng cộng số tiền phạt chưa thu: {total_fine:,.0f} VND")
            print(f"{'='*85}")

        except Exception as err:
            print(f"Lỗi truy vấn: {err}")
        finally:
            cursor.close()
            conn.close()
