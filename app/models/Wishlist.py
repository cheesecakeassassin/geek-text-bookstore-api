from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

# Wishlist class that has a name, holds the book id and the username of the user that it belongs to
class Wishlist(Base, SerializerMixin):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    wishlist_name = Column(String(50), nullable=True, unique=True)
    username = Column(String(50), ForeignKey('users.username'), nullable=False) 
    books = relationship('Book')