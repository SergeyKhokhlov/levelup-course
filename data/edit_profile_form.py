from wtforms import StringField, PasswordField, SubmitField, FileField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    old_password = PasswordField('Старый пароль')
    new_password = PasswordField('Новый пароль')
    new_password_again = PasswordField('Повторите новый пароль')
    name = StringField('Имя пользователя', validators=[DataRequired()])
    avatar = FileField("Аватар")
    submit_rus = SubmitField('Изменить')
