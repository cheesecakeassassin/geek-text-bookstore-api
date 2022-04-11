from app.db import Base
from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
import bcrypt

salt = bcrypt.gensalt()

class Card(Base, SerializerMixin):
  __tablename__ = 'cards'
  id = Column(Integer, primary_key=True)
  name = Column(String(30), nullable=False)
  card_number = Column(BigInteger, nullable=False, unique=True)
  expiration_date = Column(String(15), nullable=False)
  security_code = Column(Integer, nullable=False)
  zip_code = Column(Integer, nullable=False)
  user_id = Column(Integer , nullable=False)

#   user = relationship('User')

#   @validates('card_number')
#   def validate_carc(self, key, card_number):
#     assert len(card_number) > 14

#     # Encrypt password
#     return bcrypt.hashpw(card_number.encode('utf-8'), salt)

#   @validates('security_code')
#   def validate_carc(self, key, security_code):
#     assert len(security_code) > 2

#     # Encrypt password
#     return bcrypt.hashpw(security_code.encode('utf-8'), salt)