from app.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_serializer import SerializerMixin

class Wishlist(Base, SerializerMixin):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    username = Column('username', String(50), ForeignKey('users.username')), 
    book_id = Column('book_id', Integer, ForeignKey('books.id'))