class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity  # Available quantity of the book

    def display_book_info(self):
        print(f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Available Quantity: {self.quantity}")
        
    def check_availability(self):
        return self.quantity > 0

    def update_quantity(self, quantity):
        self.quantity += quantity

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []  # List to store borrowed books

    def borrow_book(self, book):
        if book.check_availability():
            self.borrowed_books.append(book)
            book.update_quantity(-1)  # Decrease the quantity of the borrowed book
            print(f"{self.name} has borrowed '{book.title}'")
        else:
            print(f"Sorry, '{book.title}' is not available for borrowing.")

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_quantity(1)  # Increase the quantity of the returned book
            print(f"{self.name} has returned '{book.title}'")
        else:
            print(f"{self.name} does not have '{book.title}' borrowed.")

    def view_borrowed_books(self):
        if self.borrowed_books:
            print(f"{self.name}'s Borrowed Books:")
            for book in self.borrowed_books:
                print(f" - {book.title}")
        else:
            print(f"{self.name} has not borrowed any books.")

class Library:
    def __init__(self):
        self.books = []  # List to store all books in the library
        self.users = []  # List to store all users of the library

    def add_book(self, book):
        self.books.append(book)

    def register_user(self, user):
        if any(curr_user.user_id == user.user_id for curr_user in self.users):
            print("User with the same ID already exists! Try another ID.")
            return
        self.users.append(user)
        print(f"New user {user.name} added successfully!")

    def search_book_by_title(self, title):
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        return found_books

    def list_books(self):
        if self.books:
            print("Books in the Library:")
            for book in self.books:
                book.display_book_info()
        else:
            print("No books available in the library.")

    def add_new_book(self):
        book_id = int(input("Enter book ID: "))
        if any(book.book_id == book_id for book in self.books):
            print("Book with the same ID already exists, please try another ID.")
            return

        title = input("Enter book title: ")
        author = input("Enter author name: ")
        quantity = int(input("Enter the quantity of books: "))
        
        new_book = Book(book_id, title, author, quantity)
        self.add_book(new_book)
        print("Book added successfully!")
        new_book.display_book_info()

def main():
    library = Library()

    # Adding some books to the library
    book1 = Book(1, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 5)
    book2 = Book(2, "The Hobbit", "J.R.R. Tolkien", 3)
    book3 = Book(3, "1984", "George Orwell", 2)
    
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    # Registering users
    user1 = User(1, "Geek_1")
    user2 = User(2, "Geek_2")
    
    library.register_user(user1)
    library.register_user(user2)

    # Menu
    while True:
        print("\nWelcome to the Library Management System")
        print("1. View all books")
        print("2. Add books")
        print("3. Search for a book by title")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. View borrowed books")
        print("7. Add new User")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            library.list_books()

        elif choice == '2':
            library.add_new_book()

        elif choice == '3':
            title = input("Enter the book title to search: ")
            found_books = library.search_book_by_title(title)
            if found_books:
                for book in found_books:
                    book.display_book_info()
            else:
                print(f"No books found with the title '{title}'.")

        elif choice == '4':
            user_id = int(input("Enter your user ID: "))
            book_id = int(input("Enter the book ID to borrow: "))
            user = next((u for u in library.users if u.user_id == user_id), None)
            book = next((b for b in library.books if b.book_id == book_id), None)
            if user and book:
                user.borrow_book(book)
            else:
                print("Invalid user or book ID.")

        elif choice == '5':
            user_id = int(input("Enter your user ID: "))
            book_id = int(input("Enter the book ID to return: "))
            user = next((u for u in library.users if u.user_id == user_id), None)
            book = next((b for b in library.books if b.book_id == book_id), None)
            if user and book:
                user.return_book(book)
            else:
                print("Invalid user or book ID.")

        elif choice == '6':
            user_id = int(input("Enter your user ID: "))
            user = next((u for u in library.users if u.user_id == user_id), None)
            if user:
                user.view_borrowed_books()
            else:
                print("Invalid user ID.")

        elif choice == '7':
            id = int(input("Enter user id: "))
            name = input("Enter user's name: ")
            user = User(id, name)
            library.register_user(user)

        elif choice == '8':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()