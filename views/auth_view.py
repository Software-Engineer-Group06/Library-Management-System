import getpass
import os
import datetime
class AuthView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_login_menu(self):
        self.clear_screen()
        print("ONLINE LIBRARY MANAGEMENT SYSTEM")
        print("1. Login")
        print("2. Exit")
        return input("Select an option: ")

    def get_login_input(self):
        # [cite: 593] If Login is selected:
        username = input("Username: ").strip()
        # [cite: 61] Password input must be masked
        password = input("Password: ").strip()
        return username, password

    def display_login_success(self):
        print("\nLogin successful.")
        print("Redirecting to main menu...")
        # (Giả lập loading để người dùng đọc kịp thông báo)
        input("(Press Enter to continue)") 

    def display_login_fail(self):
        print("\nLogin failed.")
        print("Invalid username or password.")
        print("Please try again.")
        input() # Đợi người dùng đọc xong

    def display_first_login_prompt(self):
        """
        Thông báo phát hiện đăng nhập lần đầu
        """
        print("\nFirst login detected.")
        print("Please change your password.")

    def get_new_password_input(self):
        new_pass = getpass.getpass("Enter new password: ")
        confirm_pass = getpass.getpass("Confirm new password: ")
        return new_pass, confirm_pass

    def display_password_success(self):
        print("\nPassword changed successfully.")
        print("Redirecting to main menu...")
        input("(Press Enter to continue)")

    def display_password_mismatch(self):
        print("\nPassword mismatch.")
        print("Please re-enter the password.")