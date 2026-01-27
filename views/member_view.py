import os
from datetime import datetime

class MemberView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_register_input(self):
        self.clear_screen()
        print("REGISTER NEW MEMBER")
        
        fullname = input("Full Name (Mandatory): ").strip()
        while not fullname:
            print("Full Name is required!")
            fullname = input("Full Name (Mandatory): ").strip()

        dept = input("Department (Mandatory): ").strip()
        while not dept:
            print("Department is required!")
            dept = input("Department (Mandatory): ").strip()

        email = input("Email (Mandatory): ").strip()
        while not email:
            print("Email is required!")
            email = input("Email (Mandatory): ").strip()
            
        phone = input("Phone: ")
        m_type = input("Member Type (Student/Teacher): ")
        dob_str = input("Date of Birth (DD/MM/YYYY): ")

        try:
            dob = datetime.strptime(dob_str, '%d/%m/%Y').date()
            return {
                'fullname': fullname, 'department': dept, 'email': email,
                'phone': phone, 'member_type': m_type, 'dob': dob
            }
        except ValueError:
            print("\n[Error] Invalid Date Format. Registration Cancelled.")
            input("(Press Enter)")
            return None

    def display_register_success(self, new_id):
        print(f"\n[SUCCESS] Member registered successfully.")
        print(f"Generated Member ID: {new_id}")
        print(f"Default Password: (Date of Birth DDMMYYYY)")
        input("(Press Enter to continue)")

    def get_member_id_input(self, action=""):
        self.clear_screen()
        return input(f"Enter Member ID to {action}: ")

    def get_update_input(self, current):
        self.clear_screen()
        print(f"UPDATE MEMBER: {current['fullName']} (ID: {current['userID']})")
        print("Leave blank to keep current value.")
        
        fullname = input(f"Full Name ({current['fullName']}): ") or current['fullName']
        dept = input(f"Department ({current['Department']}): ") or current['Department']
        email = input(f"Email ({current['email']}): ") or current['email']
        phone = input(f"Phone ({current['phone']}): ") or current['phone']
        m_type = input(f"Type ({current['MemberType']}): ") or current['MemberType']
        
        dob_str = input(f"DOB ({current['dateOfBirth'].strftime('%d/%m/%Y')}): ")
        try:
            dob = datetime.strptime(dob_str, '%d/%m/%Y').date() if dob_str else current['dateOfBirth']
            return {
                'fullname': fullname, 'department': dept, 'email': email,
                'phone': phone, 'member_type': m_type, 'dob': dob
            }
        except ValueError:
            return None

    def display_msg(self, msg):
        print(f"\n>> {msg}")
        input("(Press Enter)")