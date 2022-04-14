import datetime
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


# CREATE A REVIEW LIST (ASSOCIATION TABLE - MANY TO MANY RELATIONSHIP) REVIEW TABLE LOOK AT THE LAST SECTION(FERNANDO)
bookReview = db.Table('bookReview',
                    db.Column('book_id', db.String, 
                            db.ForeignKey('book.id')),
                    db.Column('review_id', db.Integer, db.ForeignKey('review.id'))
                    )



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
    #REVIEW RELATIONSHIP TABLE HAS TO GO WITH BOOK CLASS
    bookReview = db.relationship(
       'Review', secondary=bookReview, backref='inReview')

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
###################### Book Rating and Commmenting ########################
###########################################################################


# CREATE THE SQLALCHEMY REVIEW MODEL
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(40))
    comment = db.Column(db.String(50))
    datetime = db.Column(db.String(40))
  # bookId = db.Column(db.String(40))
  #  bookReview = db.relationship(
  #      'Book', secondary=bookReview, backref='inBook')

    
    def __init__(self, rating, comment):
        self.rating = rating
        self.comment = comment
        self.datetime = datetime
    #    self.bookId = bookId
    #    self.bookReview = bookReview


# FUNCTION TO RETURN A BOOK DICTIONARY
def review_dict(new_review):
    review = {
        "id": new_review.id,
        "rating": new_review.rating,
        "comment": new_review.comment
    #   "datetime" = new_review.datetime
    }
    return review


# ADD A BOOK TO THE REVIEW'S RRATING AND COMMENTING
@app.route('/reviewList/<userName>', methods=['POST'])
def create_bookReview_input(userName):
    # Get the ID from the book's json data passed in the POST request ("id": "#")
    bookID = request.json['id']
    rating = request.json['rating']
    comment = request.json['comment']
    datetime = request.json['datetime']
    # Get the user from the DB
    # user = User.query.filter_by(name=userName).first()
    # Get the book from the DB
    book = Book.query.get(bookID)
    review = Review(rating = rating, comment = comment)
    # Add book to the user's book review
    book.bookReview.append(review)
    # Save the user's book rating into the DB
    db.session.commit()

    # Return the user's book review as json
    reviewList = []
    for book in book.bookReview:
        result = review_dict(book)
        reviewList.append(result)
    result = json.dumps(reviewList)
    return result



# GET BOOKS BY RATING AND HIGHER
@app.route('/BookRating', methods=['POST'])
# Select a list of books with sales grater than 1000
def get_book_by_rating():
    reviewList = reviewList.query.all()
    finalList = []
    reviewList = sorted(reviewList, key=lambda x: x['rating'])
    for review in reviewList:
           all_reviews = review_dict(book)
           finalList.append(all_reviews)
    result = json.dumps(finalList)
    return result


# GET BOOKS BY RATING AND AVERAGE
@app.route('/BookRating', methods=['POST'])
# Get an average of the ratings for a book
def get_book_by_rating_average():
    reviewList = reviewList.query.all()
    counter = 0
    rating_sum = 0
    for review in book.reviews:
        rating_sum += review.rating
        counter += 1
        
    return




if __name__ == '__main__':
    app.run(debug=True)







# NOTES

# scrum = Book(title='The scrum guide', description = 'this is a guide to master scrum', author = 'jhon', price = '5')
# db.session.add(scrum)
# db.session.commit()

# >>> from app import db, Book, User, Review
# >>> db.create_all()
# >>> db.drop_all()

# >>> Book.query.all()
# [<Book 1>, <Book 2>]
# >>> Book.query.get(1)




