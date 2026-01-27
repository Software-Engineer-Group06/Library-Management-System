from views.librarian_view import LibrarianView
from controllers.book_controller import BookController
from controllers.report_controller import ReportController
from controllers.circulation_controller import CirculationController
from controllers.member_controller import MemberController
class LibrarianController:
    def __init__(self):
        self.book_app = BookController()
        self.circ_app = CirculationController()
        self.report_app = ReportController()
        self.view = LibrarianView()
        self.member_app = MemberController()

    def librarian_menu(self):
        while True:
            choice = self.view.show_menu()
            
            if choice == '1': # Manage Books
                self.book_app.manage_book()
            
            elif choice == '2': # Issue Book
                self.circ_app.issue_book()
            
            elif choice == '3': # Receive Return
                self.circ_app.return_book()
            
            elif choice == '4': # Calculate Fines
                self.circ_app.check_fine()
            
            elif choice == '5': # Register Member
                self.member_app.register_member()
            
            elif choice == '6': # Update Member
                self.member_app.update_member()
            
            elif choice == '7': # Delete Member
                self.member_app.delete_member()
            
            elif choice == '8': # Reports
                self.report_app.librarian_reports()
            
            elif choice == '9': # Logout
                print("Logged out successfully.")
                break
            else:
                print("Invalid option selected.")

    def member_menu(self, member_id):
        while True:
            choice = self.view.show_member_menu()
            
            if choice == '1':
                BookController().search()
            elif choice == '2':
                CirculationController().view_history(member_id) 
            elif choice == '3':
                ReportController().member_notifications(member_id)
            elif choice == '4':
                CirculationController().reserve_book(member_id)
            elif choice == '5':
                break