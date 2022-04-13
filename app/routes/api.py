from flask import Blueprint, request, jsonify, session
from app.models import User, Card, Book
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
  userList = []
  for user in users:
    all_users = user.to_dict()
    userList.append(all_users)

  return jsonify(userList)


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
    newUser = User(
      name = data['name'],
      username = data['username'],
      email = data['email'],
      home_address = data['home_address'],
      password = data['password'],
    )

    # Save in database
    db.add(newUser)
    db.commit()
  except:
    print(sys.exc_info()[0])

    # Insert failed, so send error to front end
    db.rollback()
    return jsonify(message = 'Add user failed'), 500

  return jsonify(message = "Successfully created user",id = newUser.id, name = newUser.name, username = newUser.username, email = newUser.email, home_address = newUser.home_address, password = newUser.password)


# Update user by id
@bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).get(id)
    user.name = data['name'],
    user.username = data['username'],
    user.home_address = data['home_address'],
    user.password = data['password']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Invalid update (Note: email cannot be updated and other fields must be included)'), 404

  return '', 204

###########################################################################
############################ CARD ROUTES ##################################
###########################################################################

# Get all cards
@bp.route('/cards', methods=['GET'])
def get_all_cards():
  db = get_db()
  cards = db.query(Card).all()
  cardList = []
  for card in cards:
    all_cards = card.to_dict()
    cardList.append(all_cards)

  return jsonify(cardList)


# Add card
@bp.route('/cards', methods=['POST'])
def add_card():
  data = request.get_json()
  db = get_db()
  
  try:
    newCard = Card(
      name = data['name'],
      card_number = data['card_number'],
      expiration_date = data['expiration_date'],
      security_code = data['security_code'],
      zip_code = data['zip_code'],
      user_id = data['user_id']
    )

    # Save in database
    db.add(newCard)
    db.commit()
  except:
    print(sys.exc_info()[0])

    # Insert failed, so send error to front end
    db.rollback()
    return jsonify(message = 'Add card failed'), 500

  return jsonify(id = newCard.id, name = newCard.name, expiration_date = newCard.expiration_date, card_number = newCard.card_number, security_code = newCard.security_code, zip_code = newCard.zip_code, user_id = newCard.user_id)

###########################################################################
########################## WISHLIST ROUTES ################################
###########################################################################

# Retrieve list of books from given user's wishlist
@bp.route('/wishlist/<username>', methods=['GET'])
def get_wishlist(username):
  # Import database
  db = get_db()

  # Get the user from the DB
  user = db.query(User).filter_by(name=username).first()

  # Get the list of books
  userList = user.wishlist
  wishlist = []

  # Return the wish list as json
  for book in userList:
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
  user = db.query(User).filter_by(name=username).first()
  book = db.query(Book).get(data['id'])

  # Add book to the wish list
  user.wishlist.append(book)

  # Save the wish list into the DB
  db.commit()

  # Return the wish list as json
  result = book.to_dict()

  return jsonify(result)


# REMOVE A BOOK FROM A WISH LIST AND SEND TO SHOPPING CART
@bp.route('/wishlist/<username>', methods=['DELETE'])
def move_to_hopping_cart(username):
  # Import database
  db = get_db()
  data = request.get_json()

  # Get the user and book from the DB
  user = db.query(User).filter_by(name=username).first()
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
  user = db.query(User).filter_by(name=username).first()

  # Get the list of books
  shopping_cart_list = user.shopping_cart
  shopping_cart = []

  # Return the wish list as json
  for book in shopping_cart_list:
    result = book.to_dict()
    shopping_cart.append(result)

  return jsonify(shopping_cart)