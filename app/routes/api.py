from flask import Blueprint, request, jsonify
from app.models import User, Card, Book, Review
from datetime import datetime
from app.db import get_db
import sys

# Uses /api endpoint for all of these api routes
bp = Blueprint('api', __name__, url_prefix='/api')

###########################################################################
############################# USER ROUTES #################################
###########################################################################

# Get all users
@bp.route('/users', methods=['GET'])
def get_all_users():
  db = get_db()
  users = db.query(User).all()
  user_list = []
  for user in users:
    all_users = user.to_dict()
    user_list.append(all_users)

  return jsonify(user_list)


# Get user by id
@bp.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
  db = get_db()

  try:
    user = db.query(User).get(id)
    result = user.to_dict()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(error = "User doesn't exist"), 500

  return jsonify(result)


# Get user by username
@bp.route('/user/<username>', methods=['GET'])
def get_user_by_username(username):
  db = get_db()

  try:
    user = db.query(User).filter_by(username=username).first()
    result = user.to_dict()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(error = "User doesn't exist"), 500

  return jsonify(result)


# Add user
@bp.route('/users', methods=['POST'])
def add_user():
  data = request.get_json()
  db = get_db()
  
  try:
    # Create a new user
    new_user = User(
      name = data['name'],
      username = data['username'],
      email = data['email'],
      home_address = data['home_address'],
      password = data['password'],
    )

    # Save in database
    db.add(new_user)
    db.commit()
  except:
    print(sys.exc_info()[0])

    # Insert failed, so send error to front end
    db.rollback()
    return jsonify(message = 'Add user failed'), 500

  return jsonify(message = "Successfully created user", id = new_user.id, name = new_user.name, username = new_user.username, email = new_user.email, home_address = new_user.home_address, password = new_user.password)


# Update user by id
@bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).get(id)
    user.name = data['name']
    user.username = data['username']
    user.home_address = data['home_address']
    user.password = data['password']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Invalid update (Note: email cannot be updated and other fields must be included)'), 404

  return jsonify(message = "Successfully updated")

###########################################################################
############################ CARD ROUTES ##################################
###########################################################################

# Get all cards
@bp.route('/cards', methods=['GET'])
def get_all_cards():
  db = get_db()
  cards = db.query(Card).all()
  card_list = []
  for card in cards:
    all_cards = card.to_dict()
    card_list.append(all_cards)

  return jsonify(card_list)


# Add card
@bp.route('/cards', methods=['POST'])
def add_card():
  data = request.get_json()
  db = get_db()
  
  try:
    new_card = Card(
      name = data['name'],
      card_number = data['card_number'],
      expiration_date = data['expiration_date'],
      security_code = data['security_code'],
      zip_code = data['zip_code'],
      user_id = data['user_id']
    )

    # Save in database
    db.add(new_card)
    db.commit()
  except:
    print(sys.exc_info()[0])

    # Insert failed, so send error to front end
    db.rollback()
    return jsonify(message = 'Add card failed'), 500

  return jsonify(id = new_card.id, name = new_card.name, expiration_date = new_card.expiration_date, card_number = new_card.card_number, security_code = new_card.security_code, zip_code = new_card.zip_code, user_id = new_card.user_id)

###########################################################################
########################## WISHLIST ROUTES ################################
###########################################################################

# Retrieve list of books from given user's wishlist
@bp.route('/wishlist/<username>', methods=['GET'])
def get_wishlist(username):
  # Import database
  db = get_db()

  # Get the user from the DB
  user = db.query(User).filter_by(username=username).first()

  # Get the list of books
  user_list = user.wishlist
  wishlist = []

  # Return the wish list as json
  for book in user_list:
    result = book.to_dict()
    wishlist.append(result)

  return jsonify(wishlist)
    
    
 # Add book to given user's wishlist
@bp.route('/wishlist/<username>', methods=['POST'])
def create_wishlist(username):
  # Import database
  db = get_db()
  data = request.get_json()

  # Get the user and book from the DB
  user = db.query(User).filter_by(username=username).first()
  book = db.query(Book).get(data['id'])

  # Add book to the wish list
  user.wishlist.append(book)

  # Save the wish list into the DB
  db.commit()

  # Return the wish list as json
  result = book.to_dict()

  return jsonify(result)


# Remove a book from given user's wishlist and send to shopping cart
@bp.route('/wishlist/<username>', methods=['DELETE'])
def move_to_hopping_cart(username):
  # Import database
  db = get_db()
  data = request.get_json()

  # Get the user and book from the DB
  user = db.query(User).filter_by(username=username).first()
  book = db.query(Book).get(data['id'])

  # Remove book from the wish list and send it to shopping cart
  user.wishlist.remove(book)
  user.shopping_cart.append(book)

  # Save the wish list into the DB
  db.commit()

  # Return book removed from wish list
  my_book = book.to_dict()

  return jsonify(my_book)

###########################################################################
####################### SHOPPING CART ROUTES ##############################
###########################################################################

# Display given user's shopping cart
@bp.route('/shopping-cart/<username>', methods=['GET'])
def get_shoppingcart(username):
  # Import database
  db = get_db()

  # Get the user from the DB
  user = db.query(User).filter_by(username=username).first()

  # Get the list of books
  shopping_cart_list = user.shopping_cart
  shopping_cart = []

  # Return the wish list as json
  for book in shopping_cart_list:
    result = book.to_dict()
    shopping_cart.append(result)

  return jsonify(shopping_cart)

###########################################################################
############################## BOOK ROUTES ################################
###########################################################################

# Create a book
@bp.route('/book', methods=['POST'])
def create_book():
  # Import db
  db = get_db()
  data = request.get_json()

  # Create a new book
  new_book = Book(
    book_title = data['book_title'],
    genre = data['genre'],
    author = data['author'],
    isbn = data['isbn'],
    publisher = data['publisher'],
    price = data['price'],
    year_published = data['year_published'],
    description = data['description'],
    sold_copies = data['sold_copies']
  )
  # Add book to the database
  db.add(new_book)
  db.commit()

  # Store all the book data in a variable and return all that data
  book = new_book.to_dict()

  return jsonify(book)


# Get all books
@bp.route('/books', methods=['GET'])
def get_books():
  # Import db
  db = get_db()

  # Getting books
  books = db.query(Book).all()
  book_list = []

  # Serializing every book individually
  for book in books:
    all_books = book.to_dict()
    book_list.append(all_books)

  return jsonify(book_list)


# Get a single book
@bp.route('/book/<id>', methods=['GET'])
def book_details(id):
  # Import db
  db = get_db()
  
  # Querying book by id and serializing it
  book = db.query(Book).get(id)
  my_book = book.to_dict()

  return jsonify(my_book)


# Update a book
@bp.route('/book/<id>', methods=['PUT'])
def book_update(id):
  # Import db
  db = get_db()
  data = request.get_json()

  # Query book's id
  book = db.query(Book).get(id)

  # Update book with new data
  book.book_title = data['book_title']
  book.genre = data['genre']
  book.author = data['author']
  book.rating = data['rating']
  book.isbn = data['isbn']
  book.publisher = data['publisher']
  book.price = data['price']
  book.year_published = data['year_published']
  book.description = data['description']
  book.sold_copies = data['sold_copies']

  # Add updated book to the database
  db.commit()

  return jsonify(message = "Successfully updated")


# Delete a book
@bp.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
  # Import db
  db = get_db()

  book = db.query(Book).get(id)

  db.delete(book)
  db.commit()

  result = "You deleted book " + id

  return jsonify(message = result)

###########################################################################
####################  BROWSING AND SORTING ROUTES #########################
###########################################################################

# Get books by genre
@bp.route('/books/<genre>', methods=['GET'])
def get_books_by_genre(genre):
  # Import db
  db = get_db()

  # Query books by genre
  books = db.query(Book).filter_by(genre).all()
  book_list = []

  for book in books:
    all_books = book.to_dict()
    book_list.append(all_books)

  return jsonify(book_list)


# Get top sellers
@bp.route('/top-seller-books', methods=['GET'])
def get_top_sellers():
  # Import db
  db = get_db()

  # Query all books
  books = db.query(Book).all()

  book_list = []
  sorted_list = []
    
  for book in books:
    all_books = book.to_dict()
    book_list.append(all_books)

  sorted_books = sorted(book_list, key=lambda x: x['soldCopies'], reverse=True)

  # Display top 10 books
  i = 0
  for book in range(10):
    sorted_list.append(sorted_books[i])
    i += 1
    print(i)
    
  return jsonify(sorted_list)


# Get books for a particular rating or higher
@bp.route('/books/rating/<rating>', methods=['GET'])
def get_book_by_rating(rating):
  # Import db
  db = get_db()

  # Query all books
  books = db.query(Book).all()
  books_by_rating = []

  for book in books:
    if book.rating >= rating:
      all_books = book.to_dict()
      books_by_rating.append(all_books)

  return jsonify(books_by_rating)


# Get books by position in record set
@bp.route('/books/return/<record>', methods=['GET'])
# Return an X number of records
def get_books_by_x_record(record):
  # Import db
  db = get_db()

  books = db.query(Book).all()
  book_list = []

  i = 0
  for book in books:
    if i < record:
      all_books = book.to_dict()
      book_list.append(all_books)
      i += 1
    else:
      break

    return jsonify(book_list)

###########################################################################
##################### RATING AND COMMENTING ROUTES ########################
###########################################################################

# Add user rating and comments to a book
@bp.route('/reviews/<username>', methods=['POST'])
def create_book_review_input(username):
  # Import db
  db = get_db()
  data = request.get_json()

  # Get the user from the DB
  user = db.query(User).filter_by(username=username).first()

  # Get the book from the DB
  book = db.query(Book).get(data['id'])

  # Create review
  review = Review(
    rating = data['rating'], 
    comment = data['comment'],
    username = username,
    created_at = datetime.now
  )
  # Add book to the user's book review
  book.reviews.append(review)

  # Save the user's book rating into the DB
  db.commit()

  # Return the user's book review as json
  review_list = []

  for book_review in user.reviews:
    all_reviews = book_review.to_dict()
    review_list.append(all_reviews)

  return jsonify(review_list)


# Get given book's average rating based on reviews
@bp.route('/books/average/<id>', methods=['GET'])
def get_book_by_rating_average(id):
  # Import db
  db = get_db()

  # Query 
  book = db.query(Book).get(id)

  # Iterate through book's reviews to calculate average rating
  counter = 0
  rating_sum = 0
  for review in book.reviews:
    rating_sum += review.rating
    counter += 1

  average_rating = rating_sum / counter

  return jsonify(average_rating = average_rating + " for book #" + id)


# Get list of ratings/comments sorted by highest rating
@bp.route('/reviews', methods=['GET'])
def get_reviews_by_rating():
  # Import db
  db = get_db()

  reviews = db.query(Review).all()
  sorted_list = []

  sorted_reviews = sorted(reviews, key=lambda x: x['rating'])
  for review in sorted_reviews:
    all_reviews = review.to_dict()
    sorted_list.append(all_reviews)

  return jsonify(sorted_list)