from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer


# INSTANTIATE APP
app = Flask(__name__)


# DETERMINE THE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INSTANTIATE THE DATABASE MODEL
db = SQLAlchemy(app)


# CREATE THE SQLALCHEMY BOOK MODEL
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(100))
    genre = db.Column(db.String(40))
    author = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    isbn = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    price = db.Column(db.Integer())
    yearPublished = db.Column(db.Integer())
    description = db.Column(db.String(200))
    soldCopies = db.Column(db.Integer())

    # isTopSeller = db.Column(db.Boolean, default=False, server_default="false")

    def __init__(self, bookTitle, genre, author, rating, isbn, publisher, price, yearPublished, description, soldCopies):
        self.bookTitle = bookTitle
        self.genre = genre
        self.author = author
        self.rating = rating
        self.isbn = isbn
        self.publisher = publisher
        self.price = price
        self.yearPublished = yearPublished
        self.description = description
        self.soldCopies = soldCopies


# FUNCTION TO RETURN A BOOK DICTIONARY
def book_dict(new_book):
    book = {
        "id": new_book.id,
        "bookTitle": new_book.bookTitle,
        "genre": new_book.genre,
        "author": new_book.author,
        "rating": new_book.rating,
        "isbn": new_book.isbn,
        "publisher": new_book.publisher,
        "price": new_book.price,
        "yearPublised": new_book.yearPublished,
        "description": new_book.description,
        "soldCopies": new_book.soldCopies
    }
    return book


# CREATE A BOOK
@app.route('/book', methods=['POST'])
def book():

    # Received posted data and store it in variables
    bookTitle = request.json['bookTitle']
    genre = request.json['genre']
    author = request.json['author']
    rating = request.json['rating']
    isbn = request.json['isbn']
    publisher = request.json['publisher']
    price = request.json['price']
    yearPublished = request.json['yearPublished']
    description = request.json['description']
    soldCopies = request.json['soldCopies']
    # isTopSeller = bool(request.json['isTopSeller'])

    # Create a new book
    new_book = Book(bookTitle, genre, author, rating, isbn,
                    publisher, price, yearPublished, description, soldCopies)

    # Add book to the database
    db.session.add(new_book)
    db.session.commit()

    # Store all the book data in a variable and return all that data
    book = book_dict(new_book)
    return json.dumps(book)


# GET ALL BOOKS
@app.route('/books', methods=['GET'])
def get_books():
    # With sqlalchemy we don't need sql queries, we use the following format instead
    books = Book.query.all()
    bookList = []
    for book in books:
        all_books = book_dict(book)
        bookList.append(all_books)
    result = json.dumps(bookList)
    return result


# GET A SINGLE BOOK
@app.route('/book/<id>', methods=['GET'])
def book_details(id):
    book = Book.query.get(id)
    my_book = book_dict(book)
    return json.dumps(my_book)


# UPDATE A BOOK
@app.route('/bookUpdate/<id>', methods=['PUT'])
def book_update(id):
    book = Book.query.get(id)

    # Received posted data and store it in variables
    bookTitle = request.json['bookTitle']
    genre = request.json['genre']
    author = request.json['author']
    rating = request.json['rating']
    isbn = request.json['isbn']
    publisher = request.json['publisher']
    price = request.json['price']
    yearPublished = request.json['yearPublished']
    description = request.json['description']
    soldCopies = request.json['soldCopies']
    # Updat book with new data
    book.bookTitle = bookTitle
    book.genre = genre
    book.author = author
    book.rating = rating
    book.isbn = isbn
    book.publisher = publisher
    book.price = price
    book.yearPublished = yearPublished
    book.description = description
    book.soldCopies = soldCopies
    # Add updated book to the database
    updated_book = book_dict(book)
    db.session.commit()

    return json.dumps(updated_book)


# DELETE A BOOK
@app.route('/bookDelete/<id>', methods=['DELETE'])
def dele_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    result = "You deleted book " + id
    return result


###########################################################################
#################  BOOK BROWSING AND SORTING FEATURE ######################
###########################################################################

# GET BOOKS BY GENRE
@app.route('/booksGenre', methods=['POST'])
def get_books_by_genre():
    genre = request.json['genre']
    books = Book.query.filter_by(genre=request.json['genre']).all()
    bookList = []
    for book in books:
        all_books = book_dict(book)
        bookList.append(all_books)
    result = json.dumps(bookList)
    return result


# GET THE TOP SELLERS
@app.route('/topSellerBooks', methods=['GET'])
def get_top_sellers():
    books = Book.query.all()
    bookList = []
    sortedList = []
    count = 0
    for book in books:
        all_books = book_dict(book)
        bookList.append(all_books)
    sortedBooks = sorted(bookList, key=lambda x: x['soldCopies'], reverse=True)
    # DISPLAY TOP 10
    i = 0
    for book in range(10):
        sortedList.append(sortedBooks[i])
        i += 1
        print(i)
    result = json.dumps(sortedList)
    return result


# GET BOOKS BY RATING AND HIGHER
@app.route('/BookRating', methods=['POST'])
# Select a list of books with sales grater than 1000
def get_book_by_rating():
    ratingPicked = request.json['rating']
    books = Book.query.all()
    bookList = []
    for book in books:
        if book.rating >= ratingPicked:
            all_books = book_dict(book)
            bookList.append(all_books)
    sortedBooks = sorted(bookList, key=lambda x: x['rating'])
    result = json.dumps(sortedBooks)
    return result


# GET BOOKS BY POSITION IN THE RECORD SET
# (in POSTMAN, inside the POST body use 'record' as key and any value
# where value is the number of records in the list returned)
@app.route('/BooksByXRecord', methods=['POST'])
# Return an X number of records
def get_book_by_x_record():
    xrecord = request.json['record']
    books = Book.query.all()
    bookList = []
    i = 0
    for book in books:
        if i < xrecord:
            all_books = book_dict(book)
            bookList.append(all_books)
            i += 1
        else:
            break
    result = json.dumps(bookList)
    return result


###########################################################################
#################### PROFILE MANAGEMENT FEATURE ###########################
###########################################################################
#id = db.Column(db.Integer, primary_key=True)
# CREATE THE SQLALCHEMY USER MODEL
#


# Must be able to create a User with username(email), password and optional fields  (name, email address, home
# address)
# Must be able to retrieve a User Object and its fields by their username


# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)


# NOTES

# scrum = Book(title='The scrum guide', description = 'this is a guide to master scrum', author = 'jhon', price = '5')
# db.session.add(scrum)
# db.session.commit()

# >>> from app import db, Book
# >>> db.create_all()
# >>> db.drop_all()

# >>> Book.query.all()
# [<Book 1>, <Book 2>]
# >>> Book.query.get(1)
