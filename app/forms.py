from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField #string field - строка, submit field - кнопка,
# password field - пароль, всё вместе причиндалы для вводо
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError # DataRequired - обязательное поле ввода?
# length - длина строки, equal to - сравнение пароля validation error - исключение ошибки
from app.models import User #импортируем модель пользователя файл создали сами

class RegistrationForm(FlaskForm): #создаем форму регистрации
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')
    # confirm password  подтверждение пароля equal to повторное введение пароля
    #submit - кнопка отправки формы
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #обращаемся к базе данных ,
        # с помощью фильтра, ищем пользователя с таким именем
        if user:
            raise ValidationError('Такой пользователь уже существует. Пожалуйста, выберите другое имя.') #raise - исключение ошибки


class LoginForm(FlaskForm): #форма логина
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти') #submit - кнопка отправки формы

