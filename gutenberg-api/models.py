# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association Tables
book_authors = Table(
    'books_book_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('author_id', Integer, ForeignKey('books_author.id'))
)

book_subjects = Table(
    'books_book_subjects', Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('subject_id', Integer, ForeignKey('books_subject.id'))
)

book_bookshelves = Table(
    'books_book_bookshelves', Base.metadata,
    Column('book_id', Integer, ForeignKey('books_book.id')),
    Column('bookshelf_id', Integer, ForeignKey('books_bookshelf.id'))
)

class Book(Base):
    __tablename__ = 'books_book'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    download_count = Column(Integer)

    authors = relationship("Author", secondary=book_authors, back_populates="books")
    subjects = relationship("Subject", secondary=book_subjects, back_populates="books")
    bookshelves = relationship("Bookshelf", secondary=book_bookshelves, back_populates="books")
    formats = relationship("Format", back_populates="book")


class Author(Base):
    __tablename__ = 'books_author'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary=book_authors, back_populates="authors")


class Subject(Base):
    __tablename__ = 'books_subject'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary=book_subjects, back_populates="subjects")


class Bookshelf(Base):
    __tablename__ = 'books_bookshelf'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", secondary=book_bookshelves, back_populates="bookshelves")


class Format(Base):
    __tablename__ = 'books_format'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books_book.id'))
    mime_type = Column(String)
    url = Column(String)

    book = relationship("Book", back_populates="formats")
