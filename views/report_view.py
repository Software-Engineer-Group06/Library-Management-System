from controllers.report_controller import ReportService

def report_menu():
    service = ReportService()

    print("\nREPORT MENU")
    print("1. Overdue Books")
    print("2. Most Borrowed Books")
    print("3. Total Fines Collected")

    choice = input("Select option: ")

    if choice == "1":
        data = service.overdue_books_report()
        for r in data:
            print(r)

    elif choice == "2":
        data = service.most_borrowed_books_report()
        for title, times in data:
            print(f"{title} - {times} times")

    elif choice == "3":
        total = service.total_fines_report()
        print(f"Total fines collected: {total} VND")