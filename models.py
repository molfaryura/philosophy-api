"""
Models for Books

This module defines the database models for a book library using Flask and SQLAlchemy.

The models establish various relationships between them:
- Book and Author: Many-to-one relationship, where a book can have one author,
but an author can have multiple books.

- Book and Chapter: One-to-many relationship, where a book can have multiple chapters,
but a chapter belongs to only one book.

- Chapter and Note: One-to-one relationship, where a chapter can have one note,
and a note is associated with only one chapter.

- Book and Note: Many-to-one relationship, where a book can have multiple notes,
but a note belongs to only one book.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    """
    Model representing a book.

    Attributes:
        id (db.Column): The primary key of the book.
        title (db.Column): The title of the book.
        author_id (db.Column): The foreign key referencing the ID of the book's author.

    Relationships:
        author: Relationship to the Author model, establishing a many-to-one relationship.
        chapters: Relationship to the Chapter model, establishing a one-to-many relationship.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('book', lazy=True))

class Author(db.Model):
    """
    Model representing an author.

    Attributes:
        id (db.Column): The primary key of the author.
        name (db.Column): The name of the author.
        biography (db.Column): The biography of the author.

    Relationships:
        books: Relationship to the Book model, establishing a one-to-many relationship.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    biography = db.Column(db.Text, nullable=False)


class Chapter(db.Model):
    """
    Model representing a chapter of a book.

    Attributes:
        id (db.Column): The primary key of the chapter.
        book_id (db.Column): The foreign key referencing the ID of the associated book.
        chapter_name (db.Column): The name of the chapter.

    Relationships:
        book: Relationship to the Book model, establishing a many-to-one relationship.
        note: Relationship to the Note model, establishing a one-to-one relationship.
    """

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    chapter_name = db.Column(db.String(250), nullable=False)
    book = db.relationship('Book', backref=db.backref('chapter', lazy=True))



class Note(db.Model):
    """
    Model representing a note for a book chapter.

    Attributes:
        id (db.Column): The primary key of the note.
        book_id (db.Column): The foreign key referencing the ID of the associated book.
        chapter_id (db.Column): The foreign key referencing the ID of the associated chapter.
        content (db.Column): The content of the note.
        created_date (db.Column): The date the note was created.

    Relationships:
        book: Relationship to the Book model, establishing a many-to-one relationship.
        chapter: Relationship to the Chapter model, establishing a one-to-one relationship.
    """

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    book = db.relationship('Book', backref=db.backref('note', lazy=True))
    chapter = db.relationship('Chapter', backref=db.backref('note', uselist=False,lazy=True))
