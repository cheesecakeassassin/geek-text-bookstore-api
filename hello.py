#Creating a shopping cart instance for a user
from marshal import dumps
from tokenize import String
from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column

from SoftwareEngineering1.app import book, book_dict



# INSTANTIATE APP
app = Flask(__name__)


# DETERMINE THE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INSTANTIATE THE DATABASE MODEL
db = SQLAlchemy(app)

class User(db.Model):  #user class 
    users = db.relationship('Shopping', secondary = users, backref = 'user_shoppingCart')

# CREATE A SHOPPING TABLE IN THE DATABASE
shopping_cart = db.Table('shopping_cart',
                         db.Column('book_id', db.Integer, db.ForeignKey('book.id')) 
                         db.Column('book_name', db.String, db.ForeignKey('book.name'))
                         db.Column('user_name', db.String. db,ForeignKey('user.name'))
                        )

#UPDATE THE SHOPPING CART WITH NEW BOOK
class Shopping(db.Model):
    book_name = db.Column(db.String(100))
    book_id = db.Column(db.Integer, primary_key=True)

#ADDING THE BOOKS RETURNED FROM THE GET BOOKS METHOD TO THE SHOPPING CART OF A USER
@app.route('/addingBooks<userName>', methods = ['POST'])
def shopping_add(userName):
    user = User.query.filter_by(name=userName).first()  #we first get the user from our db
    bookNeeded = request.json['add']
    book = Book.query.get(bookNeeded)
    user.shopping_cart.append(book)  #appending the book to the user's shopping cart
    db.session.commit()   #saving it to the database
    shopping_cart = [] #creating an empty shopping cart
    for book in user.shopping_cart:
        bookAdd = book_dict(book)
        shopping_cart.append(bookAdd)   # 
    boookAdded = json.dumps(shopping_cart)
    return bookAdded

#RETRIEVE THE LIST OF BOOKS FROM THE SHOPPING CART/LIST
@app.route('/retrievingList<userName>', methods = ['GET'])
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
@app.route('/deletingBooks<userName>', methods = ['DELETE'])
def cart_deleting(userName):
    book_ID = request.json['id']
    user = User.query.filter_by(name=userName).first()
    # Get the book from the DB
    book = Book.query.get(book_ID)   #referring to the book in the database that is in the shopping cart
    #go through the shopping cart
    for Book in user.shopping_cart:
        bookdeleted = user.shopping_cart.remove(book)
        db.session.commit()
        Deleted = json.dumps(bookdeleted)
    return Deleted
    #within the shopping cart, go through the list of books
    #delete the book that the user wants from the list
