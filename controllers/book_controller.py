from models.book import BookModel
from views.book_view import BookView

class BookController:
    def __init__(self):
        self.model = BookModel()
        self.view = BookView()

    def search(self):
        keyword = self.view.get_search_keyword()
        
        results = self.model.search_books(keyword)
        
        self.view.display_search_results(results)

    def manage_book(self):
        while True:
            # Hiển thị menu Add/Update/Delete
            choice = self.view.display_manage_menu()
            
            if choice == '1': # Add
                book_data = self.view.get_book_input()
                if book_data['bookID'] and book_data['title']: # Validate sơ bộ
                    if self.model.add_book(book_data):
                        self.view.display_manage_success()
                    else:
                        self.view.display_manage_fail()
                else:
                    self.view.display_manage_fail()

            elif choice == '2': # Update
                book_id = self.view.get_book_id_input("Update")
                print("Enter new details (Title/Author):")
                title = input("New Title: ")
                author = input("New Author: ")
                
                if self.model.update_book(book_id, {'title': title, 'author': author}):
                    self.view.display_manage_success()
                else:
                    self.view.display_manage_fail()

            elif choice == '3': # Delete
                book_id = self.view.get_book_id_input("Delete")
                if self.model.delete_book(book_id):
                    self.view.display_manage_success()
                else:
                    self.view.display_manage_fail()

            elif choice == '4':
                break