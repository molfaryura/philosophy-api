import os

from flask import Flask, jsonify, request, render_template

from dotenv import load_dotenv

from models import db

app = Flask(__name__)

load_dotenv()

DB_PASSWORD = os.environ.get('DB_PWD')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{DB_PASSWORD}@localhost/postgres_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db.init_app(app)
#with app.app_context():
#    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)