from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
import bcrypt

# Generates salt used to hash password with bcrypt
salt = bcrypt.gensalt()

# Create a wishlist (association table - many-to-many relationsip)
wishlist = Table('wishlist',
    Column('username', String, ForeignKey('users.name')), 
    Column('book_id', Integer, ForeignKey('books.id'))
)

# Create a shopping cart table
shopping_cart = Table('shopping_cart',
  Column('username', String, ForeignKey('users.name')),
  Column('book_id', Integer, ForeignKey('books.id'))
)

# User class that has a one-to-many relationship with Card class
class User(Base, SerializerMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=True)
  home_address = Column(String(100), nullable=True)
  password = Column(String(100), nullable=False)
  cards = relationship('Card', cascade='all,delete,delete-orphan')
  wishList = relationship('Book', secondary=wishlist, backref='in_wishlist')
  shopping_cart = relationship('Book', secondary=shopping_cart, backref='in_shopping_cart')

  # Validation functions
  @validates('email')
  def validate_email(self, key, email):
    # Make sure email address contains @ character
    assert '@' in email

    return email

  @validates('password')
  def validate_password(self, key, password):
    assert len(password) > 4

    # Encrypt password
    return bcrypt.hashpw(password.encode('utf-8'), salt)

  def verify_password(self, password):
    return bcrypt.checkpw(
      password.encode('utf-8'),
      self.password.encode('utf-8')
    )