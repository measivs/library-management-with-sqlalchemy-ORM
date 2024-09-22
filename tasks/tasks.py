from sqlalchemy import func
from models import Book, Author

def query_max_pages_book(db):
    """Query and return the book with the maximum number of pages."""
    return db.query(Book).order_by(Book.pages.desc()).first()

def query_average_pages(db):
    """Query and return the average number of pages in books."""
    return db.query(func.avg(Book.pages)).scalar()

def query_youngest_author(db):
    """Query and return the youngest author."""
    return db.query(Author).order_by(Author.birth_date.desc()).first()

def query_authors_with_no_books(db):
    """Query and return authors with no books."""
    return db.query(Author).outerjoin(Book).filter(Book.author_id.is_(None)).all()

def query_authors_with_more_than_three_books(db):
    """Query and return five authors with more than three books."""
    return db.query(Author).join(Book).group_by(Author.id).having(func.count(Book.id) > 3).limit(5).all()
