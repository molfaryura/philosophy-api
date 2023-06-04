import os

from flask import Flask, jsonify, request, render_template

from dotenv import load_dotenv

from models import db, Books, Author

app = Flask(__name__)

load_dotenv()

DB_PASSWORD = os.environ.get('DB_PWD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@localhost/postgres_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
#with app.app_context():
#    db.create_all()

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


if __name__ == '__main__':
    app.run(debug=True)