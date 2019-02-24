from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    question_id = StringField('question_id', validators=[DataRequired()])
    answer = StringField('answer', validators=[DataRequired()])
