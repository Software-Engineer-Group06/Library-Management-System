from controllers.report_controller import ReportService
from controllers.notification_controller import NotificationService
from views.report_view import report_menu
from views.notification_view import show_notifications

def main():
    print("REPORT MENU")
    print("1. View Overdue Books Report")
    print("2. View Most Borrowed Books Report")
    print("3. Total Fines Collected Report")
    print("NOTIFY!")
    print("4. View Notification")
    choice = input("Select an option: ")
    rp_controller = ReportService()
    nt_controller = NotificationService()
    if choice == "1":
        reports = rp_controller.get_overdue_books()
    elif choice == "2":
        reports = rp_controller.get_most_borrowed_books_report()
    elif choice =="3":
        reports = rp_controller.show_all_overdue_fines()
    elif choice =="4":
        reports = nt_controller.show_notifications()
if __name__ == "__main__":
    main()

