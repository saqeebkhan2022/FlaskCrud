from flask import Flask , jsonify,request,render_template, redirect, url_for,session, flash
from math import ceil
app = Flask(__name__)
app.secret_key = 'saqeebkhan'
books = [
    {"id": 1, "title": "Clean Code: A Handbook of Agile Software Craftsmanship", "author": "Robert C. Martin"},
    {"id": 2, "title": "The Pragmatic Programmer: Your Journey to Mastery", "author": "Andrew Hunt, David Thomas"},
    {"id": 3, "title": "Design Patterns: Elements of Reusable Object-Oriented Software", "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides"},
    {"id": 4, "title": "Code Complete: A Practical Handbook of Software Construction", "author": "Steve McConnell"},
    {"id": 5, "title": "Refactoring: Improving the Design of Existing Code", "author": "Martin Fowler, Kent Beck, John Brant, William Opdyke, Don Roberts"},
    {"id": 6, "title": "The Mythical Man-Month: Essays on Software Engineering", "author": "Frederick P. Brooks Jr."},
    {"id": 7, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein"},
    {"id": 8, "title": "Programming Pearls", "author": "Jon Bentley"},
    {"id": 9, "title": "Structure and Interpretation of Computer Programs", "author": "Harold Abelson, Gerald Jay Sussman, Julie Sussman"},
    {"id": 10, "title": "Clean Architecture: A Craftsman's Guide to Software Structure and Design", "author": "Robert C. Martin"}
]


users = [
    {'email':'admin@gmail.com','password':'password'}
]

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        for user in users:
            if user['email'] == email and user['password'] == password:
                session['user'] = email
                flash('You were successfully logged in!', 'success')
                return redirect(url_for('all_books'))

        flash('Invalid email or password', 'error')

    return render_template('login.html')


#logout

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You were successfully logged out!', 'success')
    return redirect(url_for('home'))


#home page
@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')


# List of all books
@app.route('/books', methods=['GET'])
def all_books():
    if 'user' not in session:
        return redirect(url_for('home'))
        # Pagination parameters
    page = request.args.get('page', 1, type=int)  # Get current page number from query parameter
    per_page = 5  # Number of books per page
    total_books = len(books)
    total_pages = ceil(total_books / per_page)

    # Calculate start and end index for slicing
    start = (page - 1) * per_page
    end = start + per_page

    # Slice books list to get the books for the current page
    paginated_books = books[start:end]

    return render_template('books.html', books=paginated_books, page=page, total_pages=total_pages)

# Get book by Id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    for book in books:
        if book['id']==book_id:
            return book

    return {"error":"Book not found with this id"}

# Add Book
@app.route('/books/create',methods=['POST'])
def create_book():
    new_id = len(books) + 1
    new_book = {
        'id': new_id,
        'title': request.form['title'],
        'author': request.form['author']
    }
    books.append(new_book)
    return redirect(url_for('all_books'))


# update book by id
@app.route('/books/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    for book in books:
        if book['id'] == book_id:
            book['title'] = request.form.get('title', book['title'])
            book['author'] = request.form.get('author', book['author'])
            break
    return redirect(url_for('all_books'))

# Delete Book
@app.route('/books/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return redirect(url_for('all_books'))




if __name__ == '__main__':
    app.run(debug=True)