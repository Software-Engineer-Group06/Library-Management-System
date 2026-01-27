import os

class ReportView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_notifications(self, notifications):
        self.clear_screen()
        if not notifications:
            print("No new notifications.")
        else:
            print("Notifications:")
            for notif in notifications:
                date_str = notif['SentDate'].strftime('%d/%m/%Y')
                print(f"[{date_str}] {notif['Message']}")
        
        input("\n(Press Enter to return...)")

    def display_report_menu(self):
        self.clear_screen()
        print("REPORT MENU")
        print("1. Overdue Books Report")
        print("2. Most Borrowed Books Report")
        print("3. Total Fines Collected Report")
        print("4. Back")
        return input("Select an option: ")

    def display_overdue_report(self, data):
        print("\nOverdue Books Report:")
        print(f"{'Book ID':<10} {'Title':<30} {'Borrower':<20} {'Due Date'}")
        print("-" * 75)
        for row in data:
            print(f"{row['bookID']:<10} {row['Title'][:28]:<30} {row['fullName']:<20} {row['DueDate']}")
        input("\n(Press Enter to continue)")

    def display_most_borrowed_report(self, data):
        print("\nMost Borrowed Books Report:")
        for row in data:
            print(f"{row['Title']} {row['borrow_count']} times")
        input("\n(Press Enter to continue)")

    def display_total_fines_report(self, total):
        print("\nTotal Fines Collected Report:")
        print(f"Total Amount: {total:,.0f} VND")
        input("\n(Press Enter to continue)")