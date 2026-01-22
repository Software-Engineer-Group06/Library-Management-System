from models.user import UserModel
from views.auth_view import AuthView

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = AuthView()

    def run(self):
        while True:
            choice = self.view.show_login_screen()
            
            if choice == '1':
                self.handle_login()
            elif choice == '2':
                self.view.show_message("Goodbye!")
                exit()
            else:
                self.view.show_message("Invalid option!")

    def handle_login(self):
        user_id, password = self.view.get_login_input()
        user = self.model.login(user_id, password)

        if user:
            self.view.show_message(f"Login successful! Welcome {user['username']}")
            
            # TODO: Logic check First Login ở đây (dựa vào use-case)
            # if is_first_login:
            #     self.handle_change_password(user_id)
            
            # Điều hướng dựa trên Role
            if user['role'] == 1:
                # Chuyển sang Menu Librarian (Module khác sẽ làm)
                print("Redirecting to Librarian Menu...") 
                # LibrarianController().run()
            else:
                # Chuyển sang Menu Member
                print("Redirecting to Member Menu...")
                # MemberController().run()
                
            # Tạm dừng để test
            input() 
        else:
            self.view.show_message("Login failed. Invalid username or password.")