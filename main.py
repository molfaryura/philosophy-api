import os

import hashlib

from datetime import date

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash

from flask_login import LoginManager, login_user, login_required, logout_user

from dotenv import load_dotenv

from models import db, Book, Author, Note, Chapter

from admin import Admin

from forms import BookForm, AdminForm

app = Flask(__name__)

load_dotenv()

app.secret_key = os.environ.get('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

DB_PASSWORD = os.environ.get('DB_PWD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@localhost/postgres_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, user_id)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_route():
    form = AdminForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        secret_word_form = request.form['secret']

        secret_word = os.environ.get('SECRET_WORD')
        if str(hashlib.sha256(secret_word_form.encode()).hexdigest()) == secret_word:

            admin = Admin.query.filter_by(username=username).first()
            if admin and admin.check_password(password=password):
                login_user(admin)
                return redirect(url_for('admin_interface'))
            flash('Invalid username or password')
            return redirect(url_for('admin_route'))
        else:
            return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    return render_template('admin_login.html', form=form)

@app.route('/admin/interface', methods=['GET', 'POST'])
@login_required
def admin_interface():
    form = BookForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            author = form.author.data
            book = form.book.data
            chapter = form.chapter.data
            content = form.content.data

            try:
                author_name = db.session.query(Author).filter_by(name=author).first()
                book_name = db.session.query(Book).filter_by(title=book).first()
                book_chapter = db.session.query(Chapter).filter_by(book_id=book_name.id, chapter_name=chapter).first()
                db.session.query(Note).filter_by(book_id=book_name.id, chapter_id=book_chapter.id, content=content).first()
                already_exists = True
                flash("This information is already in the database")
                return redirect(url_for('admin_interface', already_exists=already_exists))
            except AttributeError:

                if not author_name:
                    new_author = Author(name=author, biography=form.bio.data)
                else:
                    new_author = author_name

                if not book_name:
                    new_book = Book(title=book, author=new_author)
                else:
                    new_book = book_name

                new_chapter = Chapter(book=new_book, chapter_name=chapter)

                new_note = Note(book=new_book, chapter=new_chapter, content=content, created_date=date.today().strftime("%Y-%m-%d"))

            try:
                db.session.add_all([new_author, new_book, new_chapter, new_note])
                db.session.commit()
                db_error = False
                flash('Form submitted successfully')
            except:
                db_error = True
                flash('Something went wrong with the database.')
            return redirect(url_for('admin_interface', db_error=db_error))

    return render_template('admin_interface.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/get/all_books')
def get_all_books():
    author_name = request.args.get('author')

    if author_name is None:
        books = db.session.query(Book).all()
    else:
        author = Author.query.filter_by(name=author_name).first()

        if author:
            books = Book.query.filter_by(author=author).all()
        else:
            return jsonify(error='This author does not exists'), 404


    if books and author_name:
        all_books = {author_name: [{'id': book.id, 'title': book.title} for book in books]}
        return jsonify(all_books), 200
    elif books and not author_name:
        all_books = [{'id': book.id, 'title': book.title} for book in books]
        return jsonify(books=all_books), 200
    else:
        return jsonify(error='Sorry, can not find any books'), 404

@app.route('/get/notes')
def get_notes():
    book_name = request.args.get('book')
    all_notes_by_book = {}
    all_notes = []

    if book_name:
        book = Book.query.filter_by(title=book_name).first()

        if book:
            notes = Note.query.filter_by(book_id=book.id).all()

            for note in notes:
                chapter = db.session.get(Chapter, note.chapter_id)
                if book.title not in all_notes_by_book:
                    all_notes_by_book[book.title] = []
                all_notes_by_book[book.title].append({'id': note.id, 'content': note.content, 'chapter': chapter.chapter_name})


            return jsonify(all_notes_by_book), 200
        else:
            return jsonify({'message': 'Book not found'}), 404
    else:
        notes = Note.query.all()

        for note in notes:
            book = db.session.get(Book, note.book_id)
            chapter = db.session.get(Chapter, note.chapter_id)
            all_notes.append({'id': note.id, 'book': book.title, 'content': note.content, 'chapter': chapter.chapter_name})

        return jsonify(all_notes), 200

db.init_app(app)
if __name__ == '__main__':
    app.run(debug=True)
