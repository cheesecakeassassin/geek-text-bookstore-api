from app.db import Base
from sqlalchemy import BigInteger, Column, ForeignKeyConstraint, Integer, String, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Card class that includes a foreign key relationship with User class
class Card(Base, SerializerMixin):
  __tablename__ = 'cards'
  id = Column(Integer, primary_key=True)
  name = Column(String(30), nullable=False)
  card_number = Column(BigInteger, nullable=False, unique=True)
  expiration_date = Column(String(15), nullable=False)
  security_code = Column(Integer, nullable=False)
  zip_code = Column(Integer, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)