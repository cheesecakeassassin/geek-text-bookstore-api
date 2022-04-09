from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db = get_db()
  
  try:
    # Create a new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    # Save in database
    db.add(newUser)
    db.commit()
  except:
    print(sys.exc_info()[0])

    # Insert failed, so send error to front end
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True
  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # Remove session variables
  session.clear()
  return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

    if user.verify_password(data['password']) == False:
      return jsonify(message = 'Incorrect credentials'), 400