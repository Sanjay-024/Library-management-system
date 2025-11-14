from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

class Book:
    def __init__(self, book_id, title, author, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity

    def check_availability(self):
        return self.quantity > 0

    def update_quantity(self, quantity):
        self.quantity += quantity

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.check_availability():
            self.borrowed_books.append(book)
            book.update_quantity(-1)
            return True
        else:
            return False

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_quantity(1)
            return True
        else:
            return False

# Initialize Library storage
books = []
users = []

# Add some sample books
books.append(Book(1, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 5))
books.append(Book(2, "The Hobbit", "J.R.R. Tolkien", 3))
books.append(Book(3, "1984", "George Orwell", 2))

# Add some sample users
users.append(User(1, "Geek_1"))
users.append(User(2, "Geek_2"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def list_books():
    return render_template('books.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        title = request.form['title']
        author = request.form['author']
        quantity = int(request.form['quantity'])
        if any(book.book_id == book_id for book in books):
            flash("Book with the same ID already exists. Please choose another ID.")
            return redirect(url_for('add_book'))
        new_book = Book(book_id, title, author, quantity)
        books.append(new_book)
        flash("Book added successfully!")
        return redirect(url_for('list_books'))
    return render_template('add_book.html')

@app.route('/users')
def list_users():
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        name = request.form['name']
        if any(user.user_id == user_id for user in users):
            flash("User with the same ID already exists. Please choose another ID.")
            return redirect(url_for('add_user'))
        new_user = User(user_id, name)
        users.append(new_user)
        flash("User added successfully!")
        return redirect(url_for('list_users'))
    return render_template('add_user.html')

@app.route('/borrow', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        book_id = int(request.form['book_id'])
        user = next((u for u in users if u.user_id == user_id), None)
        book = next((b for b in books if b.book_id == book_id), None)
        if not user:
            flash("Invalid user ID!")
            return redirect(url_for('borrow_book'))
        if not book:
            flash("Invalid book ID!")
            return redirect(url_for('borrow_book'))
        if user.borrow_book(book):
            flash(f"{user.name} has borrowed '{book.title}'.")
        else:
            flash(f"Sorry, '{book.title}' is not available for borrowing.")
        return redirect(url_for('borrow_book'))
    return render_template('borrow_book.html', users=users, books=books)

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        book_id = int(request.form['book_id'])
        user = next((u for u in users if u.user_id == user_id), None)
        book = next((b for b in books if b.book_id == book_id), None)
        if not user:
            flash("Invalid user ID!")
            return redirect(url_for('return_book'))
        if not book:
            flash("Invalid book ID!")
            return redirect(url_for('return_book'))
        if user.return_book(book):
            flash(f"{user.name} has returned '{book.title}'.")
        else:
            flash(f"{user.name} does not have '{book.title}' borrowed.")
        return redirect(url_for('return_book'))
    return render_template('return_book.html', users=users, books=books)

@app.route('/search', methods=['GET', 'POST'])
def search_book():
    found_books = []
    if request.method == 'POST':
        title = request.form['title']
        found_books = [book for book in books if title.lower() in book.title.lower()]
        if not found_books:
            flash(f"No books found with the title '{title}'.")
    return render_template('search_book.html', found_books=found_books)

@app.route('/borrowed_books/<int:user_id>')
def view_borrowed_books(user_id):
    user = next((u for u in users if u.user_id == user_id), None)
    if user:
        return render_template('borrowed_books.html', user=user)
    else:
        flash("Invalid user ID!")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
