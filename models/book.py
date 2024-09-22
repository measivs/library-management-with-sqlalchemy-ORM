from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.association import author_book_association

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    pages = Column(Integer)
    publish_date = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))

    authors = relationship("Author", secondary=author_book_association, back_populates="books")



   
