from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.association import author_book_association

class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(String)
    birth_address = Column(String)

    books = relationship("Book", secondary=author_book_association, back_populates="authors")

    