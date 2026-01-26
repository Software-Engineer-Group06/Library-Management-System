from models.book import BookModel
from views.book_view import BookView

class BookController:
    def __init__(self):
        self.model = BookModel()
        self.view = BookView()

    def run(self):
        while True:
            choice = self.view.show_menu()
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.search_book()
            elif choice == '3':
                self.delete_book()
            elif choice == '4':
                break
            else:
                self.view.show_message("Invalid option!")

    def add_book(self):
        data = self.view.get_book_input()
        if data:
            new_id = self.model.add_book(*data)
            if new_id:
                self.view.show_message(f"✅ Book added successfully! ID: {new_id}")
            else:
                self.view.show_message("❌ Failed to add book.")

    def search_book(self):
        keyword = self.view.get_search_keyword()
        results = self.model.search_books(keyword)
        self.view.display_list(results)
        input("Press Enter to continue...")

    def delete_book(self):
        book_id = self.view.get_delete_id()
        if not book_id: 
            return

        # Xác nhận trước khi xóa
        confirm = input(f"Are you sure you want to delete {book_id}? (y/n): ")
        if confirm.lower() == 'y':
            if self.model.delete_book(book_id):
                self.view.show_message("✅ Book deleted.")
            else:
                self.view.show_message("❌ Book ID not found or error.")