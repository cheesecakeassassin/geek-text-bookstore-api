#Creating a shopping cart instance for a user
from marshal import dumps
from tokenize import String
from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column

from SoftwareEngineering1.app import book, book_dict
import sqlalchemy as db



# INSTANTIATE APP
app = Flask(__name__)


# DETERMINE THE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INSTANTIATE THE DATABASE MODEL
db = SQLAlchemy(app)

###################################### BOOK CLASS ###########################################
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
    #wihsList_ID = db.Column(db.Integer, db.ForeingKey('wishList.id'))

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


################################# USER CLASS #################################################

## Wish List Table
wishList = db.Table('wishlist',
                    db.Column('user_name', db.String,
                              db.ForeignKey('user.name')),
                    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
                    )

## Shopping Cart Table
shoppingcart = db.Table('shoppingcart',
                    db.Column('user_name', db.String,
                              db.ForeignKey('user.name')),
                    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
                    )
# CREATE THE SQLALCHEMY USER MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    homeAddress = db.Column(db.String(50))
    email = db.Column(db.String(40))
    password = db.Column(db.String(40))
    wishList = db.relationship(
        'Book', secondary=wishList, backref='inWishList')
    shoppingcart = db.relationship('Book', secondary = shoppingcart, backref = 'inShoppingCart')

    def __init__(self, name, homeAddress, email, password):
        self.name = name
        self.homeAddress = homeAddress
        self.email = email
        self.password = password


# FUNCTION TO RETURN A USER DICTIONARY
def user_dict(new_user):
    user = {
        "id": new_user.id,
        "name": new_user.name,
        "homeAddress": new_user.homeAddress,
        "email": new_user.email,
        "password": new_user.password
    }
    return user


# CREATE A USER
@app.route('/user', methods=['POST'])
def user():

    # Received posted data and store it in variables
    name = request.json['name']
    homeAddres = request.json['homeAddress']
    email = request.json['email']
    password = request.json['password']
    print("this is password" + password)
    # Create a new user
    new_user = User(name, homeAddres, email, password)

    # Add a user to the database
    db.session.add(new_user)
    db.session.commit()

    # Store all the user data in a variable and return all that data
    user = user_dict(new_user)
    return json.dumps(user)


# GET A USER BY USERNAME
@app.route('/userName', methods=['POST'])
def get_user_by_name():
    name = request.json['name']
    users = User.query.filter_by(name).all()
    userList = []
    for user in users:
        all_users = user_dict(user)
        userList.append(all_users)
    result = json.dumps(userList)
    return result

    ############################## SHOPPING CART ######################################


#UPDATE THE SHOPPING CART WITH NEW BOOK
class Shopping(db.Model):
    book_name = db.Column(db.String(100))
    bookID = db.Column(db.Integer, primary_key=True)
    
    def __init__(self, book_name, bookID):
        self.book_name = book_name
        self.bookID = bookID

#ADDING THE BOOKS RETURNED FROM THE GET BOOKS METHOD TO THE SHOPPING CART OF A USER
@app.route('/addingBooks/<userName>', methods = ['POST'])
def shopping_add(userName):
    user = User.query.filter_by(name=userName).first()  #we first get the user from our db
    bookID = request.json['id']
    book = Book.query.get(bookID)
    user.shopping_cart.append(book)  #appending the book to the user's shopping cart
    db.session.commit()   #saving it to the database
    shopping_cart = [] #creating an empty shopping cart
    for book in user.shopping_cart:
        bookAdd = book_dict(book)
        shopping_cart.append(bookAdd)   # 
    bookAdded = json.dumps(shopping_cart)
    return bookAdded

#RETRIEVE THE LIST OF BOOKS FROM THE SHOPPING CART/LIST
@app.route('/retrievingList/<userName>', methods = ['GET'])
def cart_retrieving(userName):
    user = User.query.filter_by(name=userName).first()
    userList = user.shopping_cart  #storing the list in the shopping as the user's
    shopping_cart = []
    for book in shopping_cart:  #going through the cart
        books = book_dict(book)
#going through the shopping cart and get one of the book dictionaries
    bookList = json.dumps(books)
    return bookList


#DELETE A BOOK FROM THE SHOPPING CART FOR THAT USER
@app.route('/deletingBooks/<userName>', methods = ['DELETE'])
def cart_deleting(userName):
    bookID = request.json['id']
    user = User.query.filter_by(name=userName).first()
    # Get the book from the DB
    book = Book.query.get(bookID)   #referring to the book in the database that is in the shopping cart
    #go through the shopping cart
    for Book in user.shopping_cart:
        bookdeleted = user.shopping_cart.remove(book)
        db.session.commit()
        deleted = json.dumps(bookdeleted)
    return deleted
    #within the shopping cart, go through the list of books
    #delete the book that the user wants from the list
