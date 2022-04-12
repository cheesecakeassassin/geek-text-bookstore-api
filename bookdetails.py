from app import *
        
authorToBook = db.Table('authorToBook',
    db.Column('book_isbn', db.BigInteger, db.ForeignKey('book.isbn'), primary_key=True),
    db.Column('author_name', db.String(100), db.ForeignKey('author.name'), primary_key=True)
)
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    biography = db.Column(db.String(100))
    publisher = db.Column(db.String(50))
    books = db.relationship('Book', secondary=authorToBook, backref=db.backref('authors'))

    def __init__(self,name,biography,publisher):
        self.name = name
        self.biography = biography
        self.publisher = publisher

# FUNCTION TO RETURN AN AUTHOR DICTIONARY - SLS
def author_dict(new_author):
    author = {
        "id": new_author.id,
        "name": new_author.name,
        "biography": new_author.biography,
        "publisher": new_author.publisher
    }
    return author

# GET A SINGLE BOOK BASED ON ISBN
@app.route('/bookisbn/<int:isbn>', methods = ['GET'])
def book_isbn(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    book_isbn = book_dict(book)
    return json.dumps(book_isbn, indent = 4)

# GET A LIST OF BOOKS BASED ON AUTHOR
@app.route('/bookauthor/<name>', methods = ['GET'])
def book_author(name):
    authors = Book.query.filter_by(author=name).all()
    authorFilter = [book_dict(author) for author in authors]
    return json.dumps(authorFilter, indent = 4)

# CREATE A BOOK
@app.route('/admin/book', methods=['POST'])
def book():

    # Received posted data and store it in variables
    bookTitle = request.json['bookTitle']
    genre = request.json['genre']
    author = request.json['author']
    rating = request.json['rating']
    isbn = request.json['isbn']
    publisher = request.json['publisher']
    price = request.json['price']
    yearPublished = request.json['yearPublished']
    description = request.json['description']
    soldCopies = request.json['soldCopies']
    # isTopSeller = bool(request.json['isTopSeller'])

    # Create a new book
    new_book = Book(bookTitle, genre, author, rating, isbn,
                    publisher, price, yearPublished, description, soldCopies)

    # Add book to the database
    db.session.add(new_book)
    db.session.commit()

    # Store all the book data in a variable and return all that data
    book = book_dict(new_book)
    return json.dumps(book)

# CREATE AN AUTHOR
@app.route('/admin/author', methods=['POST'])
def author():

    # Received posted data and store it in variables
    name = request.json['name']
    biography = request.json['biography']
    publisher = request.json['publisher']

    # Create a new author
    new_author = Author(name, biography, publisher)

    # Add author to the database
    db.session.add(new_author)
    db.session.commit()

    # Store all the author data in a variable and return all that data
    author = author_dict(new_author)
    return json.dumps(author)

