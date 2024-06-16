from flask import Flask , jsonify,request
app = Flask(__name__)

books=[
    {"id" : 1,"title":"Python Tut","author":"saqeeb Khan"}
]

# List of all books
@app.route('/books')
def all_books():
    return books

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
    new_book ={'id':len(books)+1,'title':request.json['title'],'author':request.json['author']}
    books.append(new_book)
    return new_book


# update book by id
@app.route('/books/update/<int:book_id>',methods=['PUT'])
def update_book(book_id):
    for book in books:
        if book['id']==book_id:
            book['title']=request.json['title']
            book['author'] = request.json['author']
            return book
    return {"error":" Book not found"}

# Delete Book
@app.route('/books/delete/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id']== book_id:
            books.remove(book)
            return {"error":"Book deleted with id :" + str(book_id)}
    return {"error": "Book not found with id :" + str(book_id)}




if __name__ == '__main__':
    app.run(debug=True)