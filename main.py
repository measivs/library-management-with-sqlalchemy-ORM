from faker import Faker
from datetime import datetime, timedelta
from database import engine, get_db
from models import Author, Book, Base
import random
import tasks

class Library:
    def __init__(self):
        self.fake = Faker()
        self.create_tables()
    
    def create_tables(self):
        """Create the database tables."""
        Base.metadata.create_all(engine)

    def random_publish_date(self, birth_date):
        """Generate a random book publishing date for an author."""
        birth_date = datetime.strptime(str(birth_date), '%Y-%m-%d') + timedelta(days=10 * 365)
        end_date = datetime.today()
        publish_date = random.randint(0, (end_date - birth_date).days)
        return (birth_date + timedelta(days=publish_date)).strftime('%Y-%m-%d')

    def add_authors(self, num_authors):
        """Add authors to the database."""
        author_id_and_birth_date = []
        with next(get_db()) as db:
            for _ in range(num_authors):
                author = Author(
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    birth_date=self.fake.date_of_birth(minimum_age=10, maximum_age=70),
                    birth_address=self.fake.address()
                )
                db.add(author)
                db.commit()
                author_id_and_birth_date.append((author.id, author.birth_date))
        return author_id_and_birth_date

    def add_books(self, num_books, author_id_and_birth_date):
        """Add books to the database."""
        with next(get_db()) as db:
            for _ in range(num_books):
                author_id, author_birth_date = random.choice(author_id_and_birth_date)
                book = Book(
                    title=self.fake.sentence(nb_words=4),
                    genre=random.choice([
                        'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Thriller', 
                        'Horror', 'Historical', 'Adventure', 'Non-Fiction', 'Biography', 
                        'Self-Help', 'Drama', 'Poetry', 'Classic', 'Graphic Novel', 'Young Adult'
                    ]),
                    pages=random.randint(25, 1200),
                    publish_date=self.random_publish_date(author_birth_date),
                    author_id=author_id
                )
                db.add(book)
            db.commit()

    def run(self):
        """Run the library operations."""
        author_id_and_birth_date = self.add_authors(500)
        self.add_books(1000, author_id_and_birth_date)

        with next(get_db()) as db:
            max_pages_book = tasks.query_max_pages_book(db)
            print(f"Book with max pages:\nID: {max_pages_book.id}\nTitle: {max_pages_book.title}\nPages: {max_pages_book.pages}")

            avg_pages = tasks.query_average_pages(db)
            print(f"The average number of pages in books is {round(avg_pages)}.")

            youngest_author = tasks.query_youngest_author(db)
            print(f"The youngest author is {youngest_author.first_name} {youngest_author.last_name} who was born on {youngest_author.birth_date}.")

            authors_with_no_books = tasks.query_authors_with_no_books(db)
            print("Authors with no books:")
            for author in authors_with_no_books:
                print(f"{author.first_name} {author.last_name}")

            five_authors = tasks.query_authors_with_more_than_three_books(db)
            print('5 Authors with more than 3 books:')
            for author in five_authors:
                print(f"{author.first_name} {author.last_name}")


if __name__ == "__main__":
    library = Library()
    library.run()
