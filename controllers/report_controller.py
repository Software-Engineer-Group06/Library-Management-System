from models.report import ReportModel
from views.report_view import ReportView

class ReportController:
    def __init__(self):
        self.model = ReportModel()
        self.view = ReportView()

    def member_notifications(self, member_id):
        """Dành cho Member xem thông báo"""
        notifs = self.model.get_member_notifications(member_id)
        self.view.display_notifications(notifs)

    def librarian_reports(self):
        """Dành cho Librarian xem báo cáo"""
        # Trigger tạo thông báo tự động (Background task simulation)
        self.model.generate_due_date_reminders()

        while True:
            choice = self.view.display_report_menu()
            
            if choice == '1': # Overdue Books
                data = self.model.get_overdue_books()
                self.view.display_overdue_report(data)
                
            elif choice == '2': # Most Borrowed
                data = self.model.get_most_borrowed_books()
                self.view.display_most_borrowed_report(data)
                
            elif choice == '3': # Total Fines
                total = self.model.get_total_fines_collected()
                self.view.display_total_fines_report(total)
                
            elif choice == '4':
                break