from app.db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy_serializer import SerializerMixin

# Review class that handles user ratings and comments for books
class Review(Base, SerializerMixin):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(String(40))
    comment = Column(String(100))
    user_username = Column(String(50), ForeignKey('users.username'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=True)