from models.user import UserModel
from views.auth_view import AuthView
from controllers.librarian_controller import LibrarianController

class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.view = AuthView()

    def run(self):
        while True:
            # 1. HIỆN MENU CHÍNH (Chọn 1 hoặc 2)
            # Hàm này chỉ trả về 1 biến 'choice'
            choice = self.view.show_login_screen()
            
            if choice == '1':
                # 2. NGƯỜI DÙNG CHỌN LOGIN -> MỚI HIỆN FORM NHẬP
                self.handle_login()
            elif choice == '2':
                print("Exiting system...")
                break
            else:
                self.view.show_message("Invalid selection! Please try again.")

    def handle_login(self):
        try:
            user_id, password = self.view.get_login_input()
        except Exception as e:
            print(f"❌ LỖI TẠI VIEW: {e}")
            return

        # Gọi Model 
        try:
            user = self.model.login(user_id, password)
        except Exception as e:
            print(f"❌ LỖI NGHIÊM TRỌNG TRONG MODEL: {e}")
            print("👉 Gợi ý: Kiểm tra lại tên bảng 'User' hoặc kết nối Database.")
            return

        if user:
            try:
                self.view.show_message(f"Login successful! Welcome {user['fullName']}")
                 
                if user['role'] == 1:
                    lib_app = LibrarianController()
                    lib_app.run() 
                else:
                    self.view.show_message("Student/Teacher Interface is coming soon...")
            except Exception as e:
                print(f"❌ LỖI XỬ LÝ SAU LOGIN: {e}")
        else:
            self.view.show_message("Login Failed! Check UserID or Password.")