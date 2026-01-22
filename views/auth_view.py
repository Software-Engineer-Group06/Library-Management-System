import getpass # Thư viện giúp ẩn ký tự nhập password
import os

class AuthView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_login_screen(self):
        self.clear_screen()
        print("========================================")
        print("   ONLINE LIBRARY MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Login")
        print("2. Exit")
        choice = input("Select an option: ")
        return choice

    def get_login_input(self):
        print("\n--- LOGIN ---")
        user_id = input("User ID: ")
        # Sử dụng getpass để ẩn mật khẩu thành ***** hoặc không hiện gì
        password = getpass.getpass("Password: ") 
        return user_id, password

    def show_message(self, message):
        print(f"\n>> {message}")
        input("Press Enter to continue...")

    def show_change_password(self):
        print("\n--- FIRST LOGIN DETECTED ---")
        print("You must change your password.")
        new_pass = getpass.getpass("Enter new password: ")
        confirm_pass = getpass.getpass("Confirm new password: ")
        return new_pass, confirm_pass