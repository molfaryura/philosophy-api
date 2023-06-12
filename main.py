import os

from datetime import date

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash

from flask_login import LoginManager, login_user, login_required, logout_user

from dotenv import load_dotenv

from models import db, Books, Author, Notes, Chapters

from admin import Admin

from book_form import BookForm

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
    return db.session.query(Admin).get(user_id)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password=password):
            login_user(admin)
            return redirect(url_for('admin_interface'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('admin'))

    return render_template('admin_login.html')

@app.route('/admin/interface', methods=['GET', 'POST'])
@login_required
def admin_interface():
    form = BookForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            author = form.author.data
            book = form.book.data
            chapter = form.chapter.data
            bio = form.bio.data
            content = form.content.data
            current_date = date.today().strftime("%Y-%m-%d")

            new_author = Author(name=author, biography=bio)
            new_book = Books(title=book, author=new_author)
            new_chapter = Chapters(book=new_book, chapter_name=chapter)
            new_note = Notes(book=new_book, chapter=new_chapter, content=content, created_date=current_date)

            try:
                db.session.add_all([new_author, new_book, new_chapter, new_note])
                db.session.commit()
                db_error = False
                flash('Form submitted successfully')
            except:
                db_error = True
                flash('Something went wrong with the database.')
            finally:
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
    all_notes = []

    if book_name:
        book = Books.query.filter_by(title=book_name).first()

        if book:
            notes = Notes.query.filter_by(book_id=book.id).all()

            for note in notes:
                chapter = db.session.get(Chapters, note.chapter_id)
                all_notes.append({'id': note.id, 'book': book.title, 'content': note.content, 'chapter': chapter.chapter_name})

            return jsonify(all_notes), 200
        else:
            return jsonify({'message': 'Book not found'}), 404
    else:
        notes = Notes.query.all()

        for note in notes:
            book = db.session.get(Books, note.book_id)
            chapter = db.session.get(Chapters, note.chapter_id)
            all_notes.append({'id': note.id, 'book': book.title, 'content': note.content, 'chapter': chapter.chapter_name})

        return jsonify(all_notes), 200

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
