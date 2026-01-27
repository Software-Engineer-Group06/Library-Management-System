import os
class LibrarianView:
    def show_menu(self):
        print("\nLIBRARIAN MAIN MENU")
        print("1. Manage Books")
        print("2. Issue Book")
        print("3. Receive Returned Book")
        print("4. Calculate Fines")
        print("5. Register Member")
        print("6. Update Member Information")
        print("7. Delete Member")
        print("8. Generate Report")
        print("9. Logout")
        return input("Select an option: ")

    def show_member_menu(self):
        print("\nMEMBER MAIN MENU")
        print("1. Search Books")
        print("2. View Borrowing History")
        print("3. View Notifications")
        print("4. Reserve Book")
        print("5. Logout")
        return input("Select an option: ")