"""
Flask forms for book entry and admin login.

The forms are created using the Flask-WTF extension,
which provides a convenient way to define and validate forms in Flask applications.

Classes:
    BookForm: Form for creating a book entry.
    AdminForm: Form for the admin login.

"""

from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField, PasswordField

from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    """
    Form for creating a book entry.

    Attributes:
        author (StringField): The author of the book.
        book (StringField): The title of the book.
        chapter (StringField): The chapter of the book.
        bio (TextAreaField): The biography of the book's author.
        content (TextAreaField): The content of the book.
        submit (SubmitField): The submit button for the form.
    """

    author = StringField('Author', validators=[DataRequired()])
    book = StringField('Book', validators=[DataRequired()])
    chapter = StringField('Chapter', validators=[DataRequired()])
    bio = TextAreaField('Author Biography', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AdminForm(FlaskForm):
    """
    Form for the admin login.

    Attributes:
        username (StringField): The admin username.
        password (PasswordField): The admin password.
        secret (StringField): A secret field for additional authentication.
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    secret = StringField('Secret', validators=[DataRequired()])
