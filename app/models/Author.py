from enum import unique
from app.db import Base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin

author_to_book = Table('author_to_book',
    Base.metadata,
    Column('isbn', BigInteger, ForeignKey('books.isbn'), primary_key=True),
    Column('name', String(100), ForeignKey('authors.name'), primary_key=True)
)

class Author(Base, UserMixin, SerializerMixin):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    biography = Column(String(200))
    publisher = Column(String(50))
    books = relationship('Book', secondary=author_to_book, backref='in_authors')