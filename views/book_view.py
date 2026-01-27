import os

class BookView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_search_keyword(self):
        self.clear_screen()
        print("SEARCH BOOKS")
        # Enter search keyword (Title / Author / ISBN / Category):
        return input("Enter search keyword (Title / Author / ISBN / Category): ")

    def display_search_results(self, books):
        print("\nSearch Results:")
        if not books:
            # Output Interface - No results 
            print("No matching books found.")
        else:
            for book in books:
                print(f"Book ID: {book['bookID']}")
                print(f"Title: {book['title']}")
                print(f"Author: {book['author']}")
                print(f"Status: {book['status']}")
                print("-" * 20)
        
        input("\nPress Enter to return...")


    def display_manage_menu(self):
        self.clear_screen()
        print("BOOK MANAGEMENT")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. Back")
        return input("Select an option: ")

    def get_book_input(self):
        print("\n--- Enter Book Information ---")
        book_id = input("Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")
        publisher = input("Publisher: ")
        category = input("Category: ")
        shelf = input("Shelf Location: ")
        
        return {
            'bookID': book_id, 'title': title, 'author': author,
            'ISBN': isbn, 'publisher': publisher, 
            'category': category, 'shelfLocation': shelf
        }

    def get_book_id_input(self, action_name):
        return input(f"\nEnter Book ID to {action_name}: ")

    def display_manage_success(self):
        print("\nBook information processed successfully.")
        input("(Press Enter to continue)")

    def display_manage_fail(self):
        print("\nOperation failed.")
        print("Invalid or missing book information.")
        input("(Press Enter to continue)")