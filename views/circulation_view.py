import os
from controllers.circulation_controller import CirculationController
from datetime import datetime

class CirculationView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def __init__(self):
        self.controller = CirculationController()

    def display_issue_book(self):
        """Interface 12: Book Issue"""
        print("\n--- BOOK ISSUE INTERFACE ---")
        member_id = input("Enter Member ID: ")
        book_id = input("Enter Book ID: ")
        
        print("Enter Due Date (YYYY-MM-DD) [Press Enter for 14 days]: ", end="")
        manual_due_date = input().strip()
        
        # Gọi controller xử lý
        success, message = self.controller.process_borrowing(
            member_id, book_id, manual_due_date if manual_due_date else None
        )
        
        if success:
            print(f"\nBook issued successfully.\n{message}")
        else:
            print(f"\nIssue failed.\n{message}")

    def display_receive_book(self):
        """Interface 13: Book Return"""
        print("\n--- BOOK RETURN INTERFACE ---")
        book_id = input("Enter Book ID to return: ")
        
        # Gọi controller xử lý trả sách
        # Controller trả về (success, fine_amount, late_days, message)
        success, fine_amount, late_days, message = self.controller.process_returning(book_id)
        
        if success:
            # Nếu có phạt (late), in dòng hệ thống + chi tiết phạt theo đặc tả
            if fine_amount > 0:
                print(f"\n>> System detects Return Date: {datetime.now().strftime('%Y-%m-%d')}")
                print("Book returned successfully.")
                print(f"Late days: {late_days}")
                print(f"Fine amount: {fine_amount:,.0f} VND")
            else:
                # Trả đúng hạn
                print("\nBook returned successfully.")
        else:
            print(f"\nReturn failed. {message}")

    def display_calculate_fines(self):
        """Interface 14: Fine Calculation"""
        print("\n--- FINE CALCULATION INTERFACE ---")
        trans_id = input("Enter Transaction ID: ")
        
        # Hiển thị chi tiết
        success, result = self.controller.view_fine_details(trans_id)
        
        if success:
            print(f"\n{result}")
        else:
            print(f"\n{result}")