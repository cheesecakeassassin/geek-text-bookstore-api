from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


# CREATE THE SQLALCHEMY USER MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    home_address = db.Column(db.String(50))
    email = db.Column(db.String(40))
    password = db.Column(db.String(40))
    wishlist = db.relationship(
        'Book', secondary=wishlist, backref='inWishlist')

    def __init__(self, name, home_address, email, password):
        self.name = name
        self.home_address = home_address
        self.email = email
        self.password = password


# CREATE THE SQLALCHEMY CREDIT CARD MODEL
class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    card_number = db.Column(db.Integer, nullable = False, unique = True)
    expiration_date = db.Column(db.Integer, nullable = False)
    security_code = db.Column(db.Integer, nullable = False)
    zip_code = db.Column(db.Integer, nullable = False)

    def __init__(self, name, card_number, expiration_date, security_code, zip_code):
        self.name = name
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.security_code = security_code
        self.zip_code = zip_code


# FUNCTION TO RETURN A USER DICTIONARY
def user_dict(new_user):
    user = {
        "id": new_user.id,
        "name": new_user.name,
        "home_address": new_user.home_address,
        "email": new_user.email,
        "password": new_user.password
    }
    return user


# FUNCTION TO RETURN A CREDIT CARD DICTIONARY
def card_dict(new_card):
    card = {
        "id": new_card.id,
        "name": new_card.name,
        "card_number": new_card.card_number,
        "expiration_date": new_card.expirtation_date,
        "security_code": new_card.security_code,
        "zip_code": new_card.zip_code
    }
    return card


# CREATE A USER
@app.route('/user', methods=['POST'])
def user():

    # Received posted data and store it in variables
    name = request.json['name']
    home_address = request.json['home_address']
    email = request.json['email']
    password = request.json['password']
    print("this is password" + password)
    # Create a new user
    new_user = User(name, home_address, email, password)

    # Add a user to the database
    db.session.add(new_user)
    db.session.commit()

    # Store all the user data in a variable and return all that data
    user = user_dict(new_user)
    return json.dumps(user)


# GET A USER BY USERNAME
@app.route('/user', methods=['POST'])
def get_user_by_name():
    name = request.json['name']
    users = User.query.filter_by(name).all()
    userList = []
    for user in users:
        all_users = user_dict(user)
        userList.append(all_users)
    result = json.dumps(userList)
    return result

if __name__ == "__main__":
    app.run(debug = True)
    app.run(host="0.0.0.0")