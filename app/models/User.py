from app.db import Base
from marshmallow import Schema, fields
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
import bcrypt

salt = bcrypt.gensalt()

class User(Base, SerializerMixin):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=True)
  home_address = Column(String(100), nullable=True)
  password = Column(String(100), nullable=False)

  cards = relationship('Card', cascade='all,delete,delete-orphan')

# class UserSchema(Schema):
#   name = fields.Str()
#   username = fields.Str()
#   email = fields.Str()
#   home_address = fields.Str()
#   passowrd = fields.Str()
#   card_id = fields.Nested('CardSchema')

  # @validates('email')
  # def validate_email(self, key, email):
  #   # Make sure email address contains @ character
  #   assert '@' in email

  #   return email

  # @validates('password')
  # def validate_password(self, key, password):
  #   assert len(password) > 4

  #   # Encrypt password
  #   return bcrypt.hashpw(password.encode('utf-8'), salt)

  # def verify_password(self, password):
  #   return bcrypt.checkpw(
  #     password.encode('utf-8'),
  #     self.password.encode('utf-8')
  #   )