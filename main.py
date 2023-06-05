import os

from flask import Flask, jsonify, request, render_template

from dotenv import load_dotenv

from models import db, Books, Author, Notes, Chapters

app = Flask(__name__)

load_dotenv()

DB_PASSWORD = os.environ.get('DB_PWD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@localhost/postgres_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get/all_books')
def get_all_books():
    author_name = request.args.get('author')

    if author_name is None:
        books = db.session.query(Books).all()
    else:
        author = Author.query.filter_by(name=author_name).first()

        if author:
            books = Books.query.filter_by(author=author).all()
        else:
            return jsonify(error='This author does not exists'), 404


    if books:
        all_books = [{'id': book.id, 'title': book.title} for book in books]
        return jsonify(books=all_books), 200
    else:
        return jsonify(error='Sorry, can not find any books'), 404

@app.route('/get/notes')
def get_notes():
    book_name = request.args.get('book')

    if book_name:
        book = Books.query.filter_by(title=book_name).first()

        if book:
            notes = Notes.query.filter_by(book_id=book.id).all()
            all_notes = []

            for note in notes:
                chapter = Chapters.query.get(note.chapter_id)
                all_notes.append({'id': note.id, 'book': book.title, 'content': note.content, 'chapter': chapter.chapter_name})

            return jsonify(all_notes), 200
        else:
            return jsonify({'message': 'Book not found'}), 404
    else:
        return jsonify({'message': 'Please provide the book name as a query parameter'}), 400


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
