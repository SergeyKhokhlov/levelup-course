from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('пароль', validators=[DataRequired()])
    password_again = PasswordField('повторите пароль', validators=[DataRequired()])
    name = StringField('имя пользователя', validators=[DataRequired()])
    submit = SubmitField('войти')
