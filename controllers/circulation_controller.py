from models.circulation import CirculationModel
from views.circulation_view import CirculationView
import os
class CirculationController:
    def __init__(self):
        self.model = CirculationModel()
        self.view = CirculationView()

    def issue_book(self):
        member_id, book_id, due_date_db, due_date_display = self.view.get_issue_input()
        
        if not member_id:
            self.view.display_issue_fail("Invalid Date Format")
            return

        eligible, message = self.model.check_eligibility(member_id)
        if not eligible:
            self.view.display_issue_fail(message)
            return

        success, msg = self.model.issue_book(member_id, book_id, due_date_db)
        if success:
            self.view.display_issue_success(due_date_display)
        else:
            self.view.display_issue_fail(msg)
    def view_history(self, member_id):
        history = self.model.get_borrowing_history(member_id)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Borrowing History:")
        if not history:
            print("No borrowing history available.")
        else:
            for rec in history:
                r_date = rec['ReturnDate'] if rec['ReturnDate'] else "Not returned"
                print(f"Transaction ID: {rec['TransID']}") 
                print(f"Book Title: {rec['Title']}")       
                print(f"Issue Date: {rec['IssueDate']}")   
                print(f"Due Date: {rec['DueDate']}")       
                print(f"Return Date: {r_date}")            
                print("-" * 20)
        input("(Press Enter)")
    def check_fine(self):
        trans_id = self.view.get_fine_check_input()
        
        fine_data = self.model.get_fine_details(trans_id)
        
        if fine_data:
            confirm_pay = self.view.display_fine_details(fine_data)
            
            if confirm_pay:
                if self.model.pay_fine(fine_data['FineID']):
                    self.view.display_payment_success()
                else:
                    self.view.display_issue_fail("Payment Error") # Tái sử dụng hàm báo lỗi
            else:
                if not fine_data['Paid']:
                    print("\nPayment skipped.")
                    input("(Press Enter)")
        else:
            self.view.display_fine_not_found()


    def reserve_book(self, member_id):
        """Thực thi Use Case Reserve Book"""
        # Nhập Book ID
        book_id = self.view.get_reserve_input()
        
        # Gọi Model xử lý (Kiểm tra sách Issued chưa, check trùng lặp...)
        success, msg = self.model.reserve_book(member_id, book_id)
        
        if success:
            self.view.display_reserve_success(msg)
        else:
            self.view.display_reserve_fail(msg)
    def return_book(self):
        book_id = self.view.get_return_input()
        
        result = self.model.return_book(book_id)
        
        if result:
            self.view.display_return_success(result)
        else:
            self.view.display_return_fail()