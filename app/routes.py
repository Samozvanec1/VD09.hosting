from flask import render_template, redirect, url_for, flash, request
from app import app, db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm

@app.route('/')
def index():
    return render_template('index.html') # формирование первой страницы (домашней страницы)
@app.route('/clicker')
@login_required
def clicker():
    return render_template('clicker.html') # формирование второй страницы (кликера)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #шифрование пароля при регистрации
        user = User(username=form.username.data, password=hashed_password) #создание нового пользователя в базе данных
        db.session.add(user)
        db.session.commit() #подтверждение изменений в базе данных (сохранение)
        flash('Ваш аккаунт был создан!', 'success')
        return redirect(url_for('login')) #перенаправление на страницу входа после регистрации
    return render_template('register.html', title='Register', form=form) #формирование страницы регистрации

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #если пользователь уже авторизован
        return redirect(url_for('clicker'))
    form = LoginForm()
    if form.validate_on_submit(): #при нажатии на кнопку "Войти" происходит проверка пароля
        user = User.query.filter_by(username=form.username.data).first() #поиск пользователя в базе данных
        if user and bcrypt.check_password_hash(user.password, form.password.data): #проверка пароля при входе
            login_user(user) #авторизация пользователя
            return redirect(url_for('index')) #перенаправление на домашнюю страницу
        else:
            flash('Что-то у вас неверно, возможно вы неверный', 'danger') #вывод сообщения об ошибке
    return render_template('login.html',form=form) #формирование страницы входа
@app.route('/logout')
def logout():# при нажатии на кнопку "Вход" происходит выход из аккаунта
    logout_user()
    return redirect(url_for('login')) #перенаправление на страницу входа

@app.route('/click') #делай клик раз два
@login_required
def click():
    current_user.clicks += 1 #при нажатии на кнопку "Клик" происходит добавление +1 к кликам пользователя
    db.session.commit() #подтверждение изменений в базе данных (сохранение)
    return redirect(url_for('clicker')) #перенаправление на страницу кликера