import os

class LibrarianView:
    def show_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== LIBRARIAN DASHBOARD ===")
        print("1. Register New Member")
        print("2. Manage Books")
        print("3. Borrow/Return Books")
        print("0. Logout")
        return input("Select: ")

    def get_member_input(self):
        print("\n--- NEW MEMBER FORM ---")
        name = input("Full Name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        dept = input("Department: ")
        
        print("Type: 1. Student | 2. Teacher")
        type_choice = input("Select: ")
        m_type = "Teacher" if type_choice == '2' else "Student"
        
        dob = input("Date of Birth (YYYY-MM-DD): ")
        return name, email, phone, dept, m_type, dob