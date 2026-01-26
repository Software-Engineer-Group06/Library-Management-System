import os
class BookView:
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        print("\n=== 📚 BOOK INVENTORY MANAGEMENT ===")
        print("1. Add New Book")
        print("2. Search Books")
        print("3. Delete Book")
        print("4. Back to Main Menu")
        return input("Select option: ")

    def get_book_input(self):
        print("\n--- ENTER BOOK DETAILS ---")
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        isbn = input("ISBN (Optional): ").strip()
        publisher = input("Publisher: ").strip()
        category = input("Category (e.g., IT, Science): ").strip()
        shelf = input("Shelf Location (e.g., A1, B2): ").strip()
        
        if not title or not author:
            print("❌ Title and Author are required!")
            return None
        return (title, author, isbn, publisher, category, shelf)

    def display_list(self, books):
        if not books:
            print("\n(No books found)")
            return

        print(f"\n{'ID':<15} | {'Title':<30} | {'Author':<20} | {'Status':<10} | {'Shelf'}")
        print("-" * 95)
        for b in books:
            # Cắt ngắn title nếu quá dài để không vỡ giao diện
            short_title = (b['title'][:27] + '..') if len(b['title']) > 27 else b['title']
            print(f"{b['bookID']:<15} | {short_title:<30} | {b['author']:<20} | {b['status']:<10} | {b['shelfLocation']}")
        print("-" * 95)

    def get_search_keyword(self):
        return input("\nEnter keyword (Title, Author, ID): ").strip()

    def get_delete_id(self):
        return input("Enter Book ID to DELETE: ").strip()

    def show_message(self, msg):
        print(f"\n>> {msg}")