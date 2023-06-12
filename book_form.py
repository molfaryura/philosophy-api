from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField

from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired()])
    book = StringField('Book', validators=[DataRequired()])
    chapter = StringField('Chapter', validators=[DataRequired()])
    bio = TextAreaField('Author Biography', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')