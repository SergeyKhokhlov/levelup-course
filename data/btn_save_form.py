from wtforms import SubmitField
from flask_wtf import FlaskForm


class Btn(FlaskForm):
    submit = SubmitField('Отправить')
