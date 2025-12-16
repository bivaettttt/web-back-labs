from flask import Blueprint, render_template, request, redirect, session
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

lab8 = Blueprint("lab8", __name__, template_folder="templates")

@lab8.route("/lab8/")
def main():
    username = current_user.login if current_user.is_authenticated else "anonymous"
    return render_template("lab8/index.html", username=username)


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        login_form = (request.form.get('login') or '').strip()
        password_form = request.form.get('password') or ''

        # Проверки из методички
        if login_form == '':
            error = 'Имя пользователя не должно быть пустым'
        elif password_form == '':
            error = 'Пароль не должен быть пустым'
        else:
            # Проверка существования пользователя
            login_exists = users.query.filter_by(login=login_form).first()
            if login_exists:
                error = 'Такой пользователь уже существует'
            else:
                password_hash = generate_password_hash(password_form)
                new_user = users(login=login_form, password=password_hash)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/lab8/')

    # GET или ошибка — возвращаем форму + сообщение
    return render_template('lab8/register.html', error=error)


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        login_form = (request.form.get('login') or '').strip()
        password_form = request.form.get('password') or ''

        # Проверки на непустые значения
        if login_form == '':
            error = 'Имя пользователя не должно быть пустым'
        elif password_form == '':
            error = 'Пароль не должен быть пустым'
        else:
            user = users.query.filter_by(login=login_form).first()

            if user:
                if check_password_hash(user.password, password_form):
                    login_user(user, remember = False)
                    return redirect('/lab8/')

            # если пользователь не найден ИЛИ пароль неверен
            error = 'Ошибка входа: логин и/или пароль неверны'

    return render_template('lab8/login.html', error=error)


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')