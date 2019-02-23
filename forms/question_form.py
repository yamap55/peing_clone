from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class QuestionForm(FlaskForm):
    question = TextAreaField('question', validators=[DataRequired()])
