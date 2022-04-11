from flask import Blueprint, request, jsonify, session
from app.models import User, Card
from app.db import get_db
import sys
bp = Blueprint('api', __name__, url_prefix='/api')

# Get all users
@bp.route('/users')
def get_all_users():
  db = get_db()
  users = db.query(User).all()
  userList = []
  for user in users:
    all_users = user.to_dict()
    userList.append(all_users)

  return jsonify(userList)


# Get user by id
@bp.route('/users/<id>')
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
@bp.route('/user/<username>')
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

  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True
  return jsonify(id = newUser.id, name = newUser.name, username = newUser.username, email = newUser.email, home_address = newUser.home_address, password = newUser.password)


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


# Remove session variables
# session.clear()

# Get all cards
@bp.route('/cards')
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