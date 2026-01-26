from models.report_notify import ReportNotifyModel
from views.report_notify_view import ReportNotifyView

class ReportNotifyController:
    def __init__(self):
        self.model = ReportNotifyModel()
        self.view = ReportNotifyView()

    def run(self):
        while True:
            choice = self.view.show_menu()
            
            if choice == '1':
                self.show_statistics()
            elif choice == '2':
                self.show_overdue()
            elif choice == '3':
                self.send_notify()
            elif choice == '4':
                break
            else:
                self.view.show_message("Invalid option!")

    def show_statistics(self):
        stats = self.model.get_library_stats()
        if stats:
            self.view.display_stats(stats)
        else:
            self.view.show_message("Error fetching statistics.")

    def show_overdue(self):
        overdue_list = self.model.get_overdue_list()
        self.view.display_overdue_list(overdue_list)
        # Hỏi user có muốn gửi thông báo nhắc nhở nhanh không (Optional)
        input("Press Enter to continue...")

    def send_notify(self):
        data = self.view.get_notify_input()
        if data:
            member_id, message = data
            if self.model.send_notification(member_id, message):
                self.view.show_message(f"✅ Notification sent to {member_id}!")
            else:
                self.view.show_message("❌ Failed to send notification (Check MemberID).")