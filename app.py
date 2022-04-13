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

# CREATE A WISH LIST (ASSOCIATION TABLE - MANY TO MANY RELATIONSHIP)
wishList = db.Table('wishlist',
                    db.Column('user_name', db.String,
                              db.ForeignKey('user.name')),
                    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))


                    )

# CREATE A SHOPPING CART TABLE
shoppingcart = db.Table('shoppingcart',
                        db.Column('user_name', db.String,
                                  db.ForeignKey('user.name')),
                        db.Column('book_id', db.Integer,
                                  db.ForeignKey('book.id'))
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
        "yearPublished": new_book.yearPublished,
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
################## BOOK BROWSING AND SORTING FEATURE ######################
###########################################################################

# GET BOOKS BY GENRE
@app.route('/booksGenre', methods=['POST'])
def get_books_by_genre():
    genre = request.json['genre']
    print(genre)
    books = Book.query.filter_by(genre=genre).all()
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

# CREATE THE SQLALCHEMY USER MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    homeAddress = db.Column(db.String(50))
    email = db.Column(db.String(40))
    password = db.Column(db.String(40))
    wishList = db.relationship(
        'Book', secondary=wishList, backref='inWishList')
    shoppingcart = db.relationship(
        'Book', secondary=shoppingcart, backref='inShoppingCart')

    # review = db.relationship(
    #    'Rating', secondary=reviewList, backref='inWishList')
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
    homeAddress = request.json['homeAddress']
    email = request.json['email']
    password = request.json['password']
    print("this is password " + password)
    # Create a new user
    new_user = User(name, homeAddress, email, password)

    # Add a user to the database
    db.session.add(new_user)
    db.session.commit()

    # Store all the user data in a variable and return all that data
    user = user_dict(new_user)
    return json.dumps(user)


# GET A USER BY USERNAME
@app.route('/userName', methods=['POST'])
def get_user_by_name():
    names = request.json['name']
    users = User.query.filter_by(name=names).all()
    userList = []
    for user in users:
        print(user)
        all_users = user_dict(user)
        userList.append(all_users)
    result = json.dumps(userList)
    return result

# Must be able to create a User with username(email), password and optional fields  (name, email address, home
# address)
# Must be able to retrieve a User Object and its fields by their username


###########################################################################
######################## WISH LIST MANAGEMENT #############################
###########################################################################


# ADD A BOOK TO THE USER'S WISH LIST
@app.route('/wishList/<userName>', methods=['POST'])
def create_wish_list(userName):
    # Get the ID from the book's json data passed in the POST request ("id": "#")
    bookID = request.json['id']
    # Get the user from the DB
    user = User.query.filter_by(name=userName).first()
    # Get the book from the DB
    book = Book.query.get(bookID)
    # Add book to the wish list
    user.wishList.append(book)
    # Save the wish list into the DB
    db.session.commit()
    # Return the wish list as json
    result = book_dict(book)
    return json.dumps(result)


# LIST OF BOOKS IN A USER'S WISH LIST
@app.route('/wishList/<userName>', methods=['GET'])
def get_wishlist(userName):
    # Get the user from the DB
    user = User.query.filter_by(name=userName).first()
    # Get the list of books
    userList = user.wishList
    wishList = []
    # Return the wish list as json
    for book in userList:
        result = book_dict(book)
        wishList.append(result)
    result = json.dumps(wishList)
    return result


# REMOVE A BOOK FROM A WISH LIST AND SEND TO SHOPPING CART
@app.route('/wishList/<userName>', methods=['DELETE'])
def move_to_hopping_cart(userName):
    # Get the ID from the book's json data passed in the POST request ("id": "#")
    bookID = request.json['id']
    # Get the user from the DB
    user = User.query.filter_by(name=userName).first()
    # Get the book from the DB
    book = Book.query.get(bookID)
    # Remove book from the wish list
    user.wishList.remove(book)
    # Send book to shopping cart
    user.shoppingcart.append(book)
    # Save the wish list into the DB
    db.session.commit()
    # Return book removed from wish list
    my_book = book_dict(book)
    return json.dumps(my_book)


# DISPLAY A USER'S SHOPPINGCART
@app.route('/shoppingcart/<userName>', methods=['GET'])
def get_shoppingcart(userName):
    # Get the user from the DB
    user = User.query.filter_by(name=userName).first()
    # Get the list of books
    shoppingCartList = user.shoppingcart
    shoppingCart = []
    # Return the wish list as json
    for book in shoppingCartList:
        result = book_dict(book)
        shoppingCart.append(result)
    result = json.dumps(shoppingCart)
    return result


# Must be able to create a wishlist of books that belongs to user and has a unique name
# Must be able to add a book to a user’s wishlisht
# Must be able to remove a book from a user’s wishlist into the user’s shopping cart
# Must be able to list the book’s in a user’s wishlist


# RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)


# NOTES

# create a database
# python
#      >>> from app import db, Book
#      >>> db.create_all()
#      >>> db.drop_all()
#      >>> exit()

# scrum = Book(title='The scrum guide', description = 'this is a guide to master scrum', author = 'jhon', price = '5')
# db.session.add(scrum)
# db.session.commit()

# >>> Book.query.all()
# [<Book 1>, <Book 2>]
# >>> Book.query.get(1)

# MANY TO MANY REALATIONSHIP
# monica=User.query.get(1)
# book = Book.query.get(2)
# monica.wishList.append(book)

# >>> book.inWishList (this will return a list and can be accessed with a loop)
# [<User 1>]
# >>> monica.wishList
# [<Book 2>]

# >>> User.query.get(1).wishList
# [<Book 2>]
# >>> Book.query.get(2).inWishList
# [<User 1>]

# remove items from the list
# monica.wishList.remove(book)


# bookReview = db.Table('reviewlist',
#                      db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
#                      db.Column('review_id', db.Integer, db.ForeignKey('review.id'))
#                      )

# bookReview = db.relationship(
#         'Review', secondary=bookReview, backref='inBook')
