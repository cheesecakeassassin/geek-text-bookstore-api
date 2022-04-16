from flask import Blueprint, request, jsonify
from app.models import User, Card, Book, Review, Author, Wishlist
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
  # Import db
  db = get_db()

  # Query all users
  users = db.query(User).all()

  # Serialize all users and append them to an array to be printed as json
  user_list = [user.to_dict() for user in users]

  return jsonify(user_list)


# Get user by id
@bp.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
  # Import db
  db = get_db()

  try:
    # Query the given user id
    user = db.query(User).get(id)
    result = user.to_dict()
  except:
    # Prints error message if unsuccessful
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(error = "User doesn't exist"), 500

  return jsonify(result)


# Get user by username
@bp.route('/user/<username>', methods=['GET'])
def get_user_by_username(username):
  # Import db
  db = get_db()

  try:
    # Query user by username then serialize result to prepare for json
    user = db.query(User).filter_by(username=username).first()
    result = user.to_dict()
  except:
    # Prints error message if unsuccessful
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(error = "User doesn't exist"), 500

  return jsonify(result)


# Add user
@bp.route('/users', methods=['POST'])
def add_user():
  # Import db
  db = get_db()
  data = request.get_json()
  
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
    # Prints error message if unsuccessful
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Add user failed'), 500

  return jsonify(message = "Successfully created user", id = new_user.id, name = new_user.name, username = new_user.username, email = new_user.email, home_address = new_user.home_address, password = new_user.password)


# Update user by id
@bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
  # Import db
  db = get_db()
  data = request.get_json()

  try:
    # Updates user fields
    user = db.query(User).get(id)
    user.name = data['name']
    user.username = data['username']
    user.home_address = data['home_address']
    user.password = data['password']

    db.commit()
  except:
    # Prints error message if unsuccessful
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
  # Import db
  db = get_db()

  # Query all cards
  cards = db.query(Card).all()

  # Serializes all cards and adds them to an array to be printed as json
  card_list = [card.to_dict() for card in cards]
  
  return jsonify(card_list)


# Add card
@bp.route('/cards', methods=['POST'])
def add_card():
  # Import db
  db = get_db()
  data = request.get_json()
  
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
    # Prints error if unsuccessful
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Add card failed'), 500

  return jsonify(id = new_card.id, name = new_card.name, expiration_date = new_card.expiration_date, card_number = new_card.card_number, security_code = new_card.security_code, zip_code = new_card.zip_code, user_id = new_card.user_id)





###########################################################################
########################## WISHLIST ROUTES ################################
###########################################################################

# Retrieve list of books from given user's wishlist
@bp.route('/wishlist/<wishlist_name>', methods=['GET'])
def get_wishlist(wishlist_name):
  # Import database
  db = get_db()

  # Get the user from the DB
  wishlist = db.query(Wishlist).filter_by(wishlist_name=wishlist_name).first()

  # Return the wish list as json
  wishlist_list = [book.to_dict() for book in wishlist.books]

  return jsonify(wishlist_list)

# Create empty wishlist for user
@bp.route('/create-wishlist/<username>', methods=['POST'])
def create_empty_wishlist(username):
  # Import database
  db = get_db()
  data = request.get_json()

  # Get the user from the DB
  user = db.query(User).filter_by(username=username).first()

  # Create empty wishlist with unique name
  new_wishlist = Wishlist(
    username = username,
    wishlist_name = data['wishlist_name']
  )
  db.add(new_wishlist)
  db.commit()
  # Get the list of books
  user_list = user.wishlists

  # Return the wish list as json
  wishlist = [book.to_dict() for book in user_list]

  return jsonify(wishlist)
    
    
# Add book to given user's wishlist
@bp.route('/wishlist/<username>', methods=['POST'])
def add_book_to_wishlist(username):
  # Import database
  db = get_db()
  data = request.get_json()

  # Get the user and book from the DB
  book = db.query(Book).get(data['book_id'])
  wishlist = db.query(Wishlist).filter_by(wishlist_name=data['wishlist_name']).one()

  # Add book to the wish list
  wishlist.books.append(book)
 
  # Save the wish list into the DB
  db.commit()

  return jsonify(wishlist.to_dict())
  # # Requery wishlists after adding new one
  # # TODO: Make more efficient in future
  # wishlists = db.query(Wishlist).all()

  # # List of wishlists
  # wishlist_list = [wishlist.to_dict() for wishlist in wishlists]
  
  # return jsonify(wishlist_list)


# Remove a book from given user's wishlist and send to shopping cart
@bp.route('/wishlist/<username>', methods=['DELETE'])
def move_to_shopping_cart(username):
  # Import database
  db = get_db()
  data = request.get_json()

  # Get the user and book from the DB
  book = db.query(Book).get(data['book_id'])
  wishlist = db.query(Wishlist).filter_by(wishlist_name=data['wishlist_name']).one()

  # Add book to the wish list
  wishlist.books.remove(book)
 
  # Save the wish list into the DB
  db.commit()

  return jsonify(wishlist.to_dict())





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

  # Get the list of books and return the wish list as json
  shopping_cart_list = user.shopping_cart
  shopping_cart = [book.to_dict() for book in shopping_cart_list]

  return jsonify(shopping_cart)


#Add book to shopping cart
@bp.route('/shopping-cart/', methods = ['POST'])
def add_to_shopping_cart():
  # Import db
  db = get_db()
  data = request.get_json()

  # User and the book they want added to the wishlist
  username = data['username']
  book_id = data['book_id']

  # We first get the user and the bookfrom our db
  user = db.query(User).filter_by(username=username).first()
  book = db.query(Book).get(book_id)

  # Appending the book to the user's shopping cart
  user.shopping_cart.append(book)

  # Saving it to the database
  db.commit()

  return jsonify(message="Successfully added book")


# Delete a book from shopping cart
@bp.route('/shopping-cart/', methods = ['DELETE'])
def delete_book_from_shopping_cart():
  # Import db
  db = get_db()
  data = request.get_json()

  # User and the book they want added to the wishlist
  username = data['username']
  book_id = data['book_id']

  # Query user and book to be deleted from shopping cart
  user = db.query(User).filter_by(username=username).first()
  book = db.query(Book).get(book_id)

  # Delete book from shopping cart
  user.shopping_cart.remove(book)

  db.commit()

  return jsonify(message = "Book #" + book_id + " deleted")





###########################################################################
######################### BOOK DETAILS ROUTES #############################
###########################################################################

# Create a book
@bp.route('/book', methods=['POST'])
def create_book():
  # Import db
  db = get_db()
  data = request.get_json()

  # Create a new book
  new_book = Book(
    title = data['title'],
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

  # Getting books and serializing every book individually
  books = db.query(Book).all()
  book_list = [book.to_dict() for book in books]

  return jsonify(book_list)


# Get a single book by isbn
@bp.route('/book/<isbn>', methods=['GET'])
def get_book_by_isbn(isbn):
  # Import db
  db = get_db()
  
  # Querying book by id and serializing it
  book = db.query(Book).filter_by(isbn=isbn).first()
  my_book = book.to_dict()

  return jsonify(my_book)


# Get a list of books based on author
@bp.route('/books/<name>', methods = ['GET'])
def get_book_by_author(name):
  # Import db
  db = get_db()

  #Query books by author name
  authors = db.query(Book).filter_by(author=name).all()
  author_filter = [author.to_dict() for author in authors]

  return jsonify(author_filter)


# Create an author
@bp.route('/author', methods=['POST'])
def create_author():
    # Import db
    db = get_db()
    data = request.get_json()

    # Create new author
    new_author = Author(
      name = data['name'],
      biography = data['biography'],
      publisher = data['publisher']
    )

    # Add author to the database
    db.add(new_author)
    db.commit()

    # Store all the author data in a variable and return all that data
    author = new_author.to_dict()
    
    return jsonify(author)


# Update a book by id
@bp.route('/book/<id>', methods=['PUT'])
def book_update(id):
  # Import db
  db = get_db()
  data = request.get_json()

  # Query book's id
  book = db.query(Book).get(id)

  # Update book with new data
  book.title = data['title']
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


# Delete a book by id
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
@bp.route('/book-genre/<genre>', methods=['GET'])
def get_books_by_genre(genre):
  # Import db
  db = get_db()

  # Query books by genre then compile them in a list to print as json
  books = db.query(Book).filter_by(genre=genre).all()
  book_list = [book.to_dict() for book in books]

  return jsonify(book_list)


# Get top sellers
@bp.route('/top-seller-books', methods=['GET'])
def get_top_sellers():
  # Import db
  db = get_db()

  # Query all books
  books = db.query(Book).all()

  book_list = [book.to_dict() for book in books]

  sorted_books = sorted(book_list, key=lambda x: x['sold_copies'], reverse=True)
  sorted_list = []
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

  # Iterates through book's review's ratings and compares with given rating
  for book in books:
    for review in book.reviews:
      if review.rating >= rating:
        all_reviews = review.to_dict()
        books_by_rating.append(all_reviews)

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
    if i < int(record):
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
@bp.route('/reviews/', methods=['POST'])
def create_book_review_input():
  # Import db
  db = get_db()
  data = request.get_json()

  # Get the user from the DB
  user = db.query(User).filter_by(username=data['user_username']).first()

  # Get the book from the DB
  book = db.query(Book).get(data['book_id'])

  # Create review
  review = Review(
    rating = data['rating'], 
    comment = data['comment'],
    user_username = data['user_username'],
    book_id = data['book_id']
  )
  # Add book to the user's book review
  book.reviews.append(review)

  # Save the user's book rating into the DB
  db.commit()

  # Return the user's book reviews as json
  review_list = [book_review.to_dict() for book_review in user.reviews]

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
    rating_sum += int(review.rating)
    counter += 1

  average_rating = rating_sum / counter

  return jsonify(book_id = id, average_rating = average_rating)


# Get list of ratings/comments sorted by highest rating
@bp.route('/reviews', methods=['GET'])
def get_reviews_by_rating():
  # Import db
  db = get_db()

  # Query all books
  books = db.query(Book).all()
  books_by_rating = []

  # Iterates through book's review's ratings and compares with given rating
  for book in books:
    for review in book.reviews:
      all_reviews = review.to_dict()
      books_by_rating.append(all_reviews)

  # Sort reviews and place in array
  sorted_reviews = sorted(books_by_rating, key=lambda x: x['rating'], reverse=True)

  return jsonify(sorted_reviews)