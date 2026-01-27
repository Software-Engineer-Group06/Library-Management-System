import os
from datetime import datetime, timedelta

class CirculationView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def get_issue_input(self):
        self.clear_screen()
        print("ISSUE BOOK (CHECK-OUT)")
        member_id = input("Enter Member ID: ")
        book_id = input("Enter Book ID: ")
        
        default_date = (datetime.now() + timedelta(days=14)).strftime('%d/%m/%Y')
        date_input = input(f"Enter Due Date (DD/MM/YYYY) [Press Enter for 14 days]: ")
        
        if not date_input.strip():
            # Return YYYY-MM-DD for Database
            return member_id, book_id, (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'), default_date
        else:
            # Convert DD/MM/YYYY to YYYY-MM-DD
            try:
                dt = datetime.strptime(date_input, '%d/%m/%Y')
                return member_id, book_id, dt.strftime('%Y-%m-%d'), date_input
            except ValueError:
                return None, None, None, None

    def display_issue_success(self, due_date_display):
        print("\nBook issued successfully.")
        print(f"Due Date: {due_date_display}")
        input("(Press Enter to continue)")

    def display_issue_fail(self, reason=""):
        print("\nIssue failed.")
        print(f"Borrowing limit exceeded or book unavailable. ({reason})")
        input("(Press Enter to continue)")

    def get_return_input(self):
        self.clear_screen()
        print("RETURN BOOK (CHECK-IN)")
        return input("Enter Book ID: ")

    def display_return_success(self, result):
        current_date_str = datetime.now().strftime('%d/%m/%Y')
        
        if result['late_days'] > 0:
            print(f"\n>> System detects Return Date: [{current_date_str}]")
            print("Book returned successfully.")
            print(f"Late days: {result['late_days']}")
            print(f"Fine amount: {result['fine_amount']:,.0f} VND")
        else:
            print("\nBook returned successfully.")
            
        input("(Press Enter to continue)")

    def display_return_fail(self):
        """Hiển thị thông báo trả sách thất bại"""
        print("\nReturn failed. Book ID not found or not currently issued.")
        input("(Press Enter to continue)")

    def get_fine_check_input(self):
        """Giao diện nhập Transaction ID để tính phạt"""
        self.clear_screen()
        print("FINE CALCULATION & PAYMENT")
        return input("Enter Transaction ID: ")

    def display_fine_details(self, data):
        """Hiển thị chi tiết tiền phạt"""
        print("\nFine Details:")
        print(f"Transaction ID: {data['TransID']}")
        print(f"Late days: {data['late_days']}")
        print(f"Fine amount: {data['Amount']:,.0f} VND")
        
        status = "Paid" if data['Paid'] else "Unpaid"
        print(f"Payment status: {status}")
        
        if not data['Paid']:
            choice = input("\nDo you want to pay this fine now? (y/n): ")
            return choice.lower() == 'y'
        return False

    def display_payment_success(self):
        print("\nFine paid successfully.")
        input("(Press Enter to continue)")

    def display_fine_not_found(self):
        print("\nNo fine record found for this Transaction ID.")
        input("(Press Enter to continue)")
    def display_history(self, history):
        """
        Hiển thị lịch sử mượn trả
        """
        self.clear_screen()
        print("BORROWING HISTORY")
        print("-" * 60)
        
        if not history:
            print("No borrowing history available.")
        else:
            # Header
            print(f"{'Book Title':<25} | {'Issue Date':<12} | {'Due Date':<12} | {'Return Date'}")
            print("-" * 60)
            for rec in history:
                # Xử lý hiển thị ngày tháng
                i_date = rec['IssueDate'].strftime('%d/%m/%Y') if rec['IssueDate'] else "N/A"
                d_date = rec['DueDate'].strftime('%d/%m/%Y') if rec['DueDate'] else "N/A"
                r_date = rec['ReturnDate'].strftime('%d/%m/%Y') if rec['ReturnDate'] else "Not returned"
                
                # Cắt ngắn tên sách nếu quá dài
                title = (rec['Title'][:22] + '..') if len(rec['Title']) > 22 else rec['Title']
                
                print(f"{title:<25} | {i_date:<12} | {d_date:<12} | {r_date}")
        
        input("\n(Press Enter to return...)")

    def get_reserve_input(self):
        """
        Giao diện nhập ID sách để đặt trước
        """
        self.clear_screen()
        print("RESERVE BOOK")
        return input("Enter Book ID to reserve: ")

    def display_reserve_success(self, msg):
        print(f"\n[SUCCESS] {msg}")
        input("(Press Enter to continue)")

    def display_reserve_fail(self, msg):
        print(f"\n[FAILED] {msg}")
        input("(Press Enter to continue)")