from flask_login import UserMixin
from app.db import Base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, BigInteger, Integer, String, Float
from sqlalchemy.orm import relationship

# Book class that holds book information
class Book(Base, UserMixin, SerializerMixin):
    __tablename__ = 'books'
    id = Column(Integer,primary_key=True)
    title = Column(String(60), nullable = False, unique = True)
    isbn = Column(BigInteger, nullable = False, unique = True)
    author = Column(String(30), nullable = False)
    publisher = Column(String(40), nullable = False)
    genre = Column(String(20), nullable = False)
    price = Column(Float, nullable = False)
    year_published = Column(Integer, nullable = False)
    description = Column(String(200), nullable = False)
    sold_copies = Column(Integer, nullable = False)
    reviews = relationship('Review')