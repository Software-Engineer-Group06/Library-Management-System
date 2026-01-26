import os

class ReportNotifyView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        print("\n=== 📊 REPORTS & NOTIFICATIONS ===")
        print("1. Library Statistics Overview")
        print("2. View Overdue List")
        print("3. Send Notification to Member")
        print("4. Back to Main Menu")
        return input("Select option: ")

    def display_stats(self, stats):
        self.clear_screen()
        print("\n=== 📈 LIBRARY DASHBOARD ===")
        print(f"📚 Total Books:      {stats['books']}")
        print(f"busts_in_silhouette Total Members:    {stats['members']}")
        print(f"🔄 Active Borrows:   {stats['borrowing']}")
        print(f"⚠️ Overdue Items:    {stats['overdue']}")
        print("============================")
        input("Press Enter to continue...")

    def display_overdue_list(self, items):
        if not items:
            print("\n✅ Good news! No overdue books found.")
        else:
            print("\n=== ⚠️ OVERDUE BORROWS LIST ===")
            print(f"{'TransID':<15} | {'Member':<20} | {'Book Title':<25} | {'Due Date'}")
            print("-" * 80)
            for i in items:
                # Cắt ngắn tên sách nếu dài quá
                title = (i['title'][:22] + '..') if len(i['title']) > 22 else i['title']
                # Format ngày tháng
                due_date = i['dueDate'].strftime("%Y-%m-%d")
                print(f"{i['transID']:<15} | {i['fullName']:<20} | {title:<25} | {due_date}")
            print("-" * 80)

    def get_notify_input(self):
        print("\n--- SEND NOTIFICATION ---")
        member_id = input("Enter Member ID: ").strip()
        message = input("Enter Message: ").strip()
        if not member_id or not message:
            print("❌ Member ID and Message are required!")
            return None
        return member_id, message

    def show_message(self, msg):
        print(f"\n>> {msg}")