from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
import datetime
import sqlalchemy
from wtforms.validators import DataRequired


class Ask_question(FlaskForm):
    title = StringField('Название:', validators=[DataRequired()])
    question = TextAreaField('Вопрос:', validators=[DataRequired()])
    theme = StringField('Тема:', validators=[DataRequired()])
    submit = SubmitField('Вперёд!')
