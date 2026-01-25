from views.librarian_view import LibrarianView
from models.member import MemberModel

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
                print("Feature managed by Member 1")
                input()
            elif choice == '3':
                print("Feature managed by Member 2")
                input()
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