from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

# note: i set many to many relationship between two tables but because i had to repeat my previous tasks,
# including having author_id in book table, no data will be inserted into author_book_association. 
author_book_association = Table(
    'author_book', 
    Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True)
)
