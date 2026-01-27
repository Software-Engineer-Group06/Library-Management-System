import sys
from models.user import UserModel
from controllers.librarian_controller import LibrarianController
from views.auth_view import AuthView

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = AuthView()
        self.current_user = None

    def run(self):
        while True:
            choice = self.view.display_login_menu()
            if choice == '1':
                self.process_login()
            elif choice == '2':
                sys.exit()

    def process_login(self):
        # Lấy input
        username, password = self.view.get_login_input()
        
        # Kiểm tra DB
        user = self.model.verify_login(username, password)
        
        if user:
            self.current_user = user
            
            # Kiểm tra First Login
            if self.model.check_first_login(user):
                self.process_force_password_change()
            else:
                self.view.display_login_success()
                self.redirect_to_dashboard(user['role'])
        else:
            self.view.display_login_fail()

    def process_force_password_change(self):
        self.view.display_first_login_message()
        
        while True:
            new_pass, confirm_pass = self.view.get_new_password_input()
            
            if new_pass == confirm_pass:
                # Update DB
                if self.model.change_password(self.current_user['userID'], new_pass):
                    self.view.display_password_success()
                    self.redirect_to_dashboard(self.current_user['role'])
                    break
            else:
                self.view.display_password_mismatch()

    def redirect_to_dashboard(self, role):
        main_ctrl = LibrarianController()
        
        if role == 1:
            main_ctrl.librarian_menu()
        else:
            # Cần pass memberID vào để load notification
            main_ctrl.member_menu(self.current_user['userID'])