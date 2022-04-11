from flask import Blueprint, request, jsonify, session, json
from app.models import User, Post, Comment, Vote
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
      password = data['password']
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

@bp.route('/comments', methods=['POST'])
def comment():
  data = request.get_json()
  db = get_db()

  try:
    # Create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment failed'), 500

  return jsonify(id = newComment.id)

@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204

@bp.route('/posts', methods=['POST'])
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
  db = get_db()

  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204