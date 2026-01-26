from views.librarian_view import LibrarianView
from models.member import MemberModel
from controllers.book_controller import BookController
from controllers.report_notify_controller import ReportNotifyController
from controllers.circulation_controller import CirculationController
class LibrarianController:
    def __init__(self):
        self.view = LibrarianView()
        self.model = MemberModel()

    def run(self):
        while True:
            choice = self.view.show_menu()
            if choice == '1':
                self.register_member()
            elif choice == '2':
                book_app = BookController()
                book_app.run()
            elif choice == '3':
                circ_app = CirculationController()
                circ_app.run()
            elif choice == '4':
                report_app = ReportNotifyController()   
                report_app.run()
            elif choice == '0':
                break

    def register_member(self):
        data = self.view.get_member_input()
        if data:
            # data là tuple chứa (name, email...) gỡ ra truyền vào model
            new_id = self.model.add_member(*data) 
            if new_id:
                print(f"SUCCESS! New Member ID: {new_id}")
                print(f"Default Password: (Date of Birth DDMMYYYY)")
            else:
                print("Failed to register.")
            input("Press Enter to return...")