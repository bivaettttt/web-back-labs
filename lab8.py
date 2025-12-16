from flask import Blueprint, render_template, request, redirect, abort
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

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

        if login_form == '':
            error = 'Имя пользователя не должно быть пустым'
        elif password_form == '':
            error = 'Пароль не должен быть пустым'
        else:
            login_exists = users.query.filter_by(login=login_form).first()
            if login_exists:
                error = 'Такой пользователь уже существует'
            else:
                password_hash = generate_password_hash(password_form)
                new_user = users(login=login_form, password=password_hash)

                db.session.add(new_user)
                db.session.commit()

                # Автоматический логин после регистрации
                login_user(new_user, remember=False)

                return redirect('/lab8/')

    return render_template('lab8/register.html', error=error)


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        login_form = (request.form.get('login') or '').strip()
        password_form = request.form.get('password') or ''

        # чекбокс: если отмечен — remember=True
        remember = request.form.get('remember') == '1'

        if login_form == '':
            error = 'Имя пользователя не должно быть пустым'
        elif password_form == '':
            error = 'Пароль не должен быть пустым'
        else:
            user = users.query.filter_by(login=login_form).first()
            if user and check_password_hash(user.password, password_form):
                login_user(user, remember=remember)
                return redirect('/lab8/')

            error = 'Ошибка входа: логин и/или пароль неверны'

    return render_template('lab8/login.html', error=error)


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    q = (request.args.get('q') or '').strip()

    query = articles.query.filter_by(login_id=current_user.id)

    if q:
        query = query.filter(
            or_(
                articles.title.ilike(f'%{q}%'),
                articles.article_text.ilike(f'%{q}%')
            )
        )

    all_articles = query.order_by(articles.id.desc()).all()
    return render_template('lab8/articles.html', articles=all_articles, q=q)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    error = None

    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        article_text = (request.form.get('article_text') or '').strip()

        if title == '':
            error = 'Заголовок не должен быть пустым'
        elif article_text == '':
            error = 'Текст статьи не должен быть пустым'
        else:
            new_article = articles(
                login_id=current_user.id,      # привязка к пользователю
                title=title,
                article_text=article_text,
                is_favorite=False,
                is_public=False,
                likes=0
            )
            db.session.add(new_article)
            db.session.commit()
            return redirect('/lab8/articles/')

    return render_template('lab8/create.html', error=error)


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    # защита: только владелец
    if article.login_id != current_user.id:
        abort(403)

    error = None

    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        article_text = (request.form.get('article_text') or '').strip()

        if title == '':
            error = 'Заголовок не должен быть пустым'
        elif article_text == '':
            error = 'Текст статьи не должен быть пустым'
        else:
            article.title = title
            article.article_text = article_text
            db.session.commit()
            return redirect('/lab8/articles/')

    return render_template('lab8/edit.html', article=article, error=error)


@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    # защита: только владелец
    if article.login_id != current_user.id:
        abort(403)

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')


@lab8.route('/lab8/public/')
def public_articles():
    q = (request.args.get('q') or '').strip()

    query = articles.query.filter_by(is_public=True)

    if q:
        query = query.filter(
            or_(
                articles.title.ilike(f'%{q}%'),
                articles.article_text.ilike(f'%{q}%')
            )
        )

    public_list = query.order_by(articles.id.desc()).all()
    return render_template('lab8/public.html', articles=public_list, q=q)


@lab8.route('/lab8/toggle_public/<int:article_id>', methods=['POST'])
@login_required
def toggle_public(article_id):
    article = articles.query.get_or_404(article_id)

    # только автор может менять публикацию
    if article.login_id != current_user.id:
        abort(403)

    article.is_public = not bool(article.is_public)
    db.session.commit()
    return redirect('/lab8/articles/')


@lab8.route('/lab8/toggle_favorite/<int:article_id>', methods=['POST'])
@login_required
def toggle_favorite(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        abort(403)

    article.is_favorite = not bool(article.is_favorite)
    db.session.commit()
    return redirect('/lab8/articles/')