from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login = session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'timur_nadrshin_knowledge_base',
            user = 'timur_nadrshin_knowledge_base',
            password = '12345'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                            error = 'Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                            error = 'Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login = login)


@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    real_name = request.form.get('real_name', '').strip()

    if not login or not password or not real_name:
        return render_template('lab5/register.html', error='Заполните все поля', login=login, real_name=real_name)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                            error = "Такой пользователь уже существует",
                            login = login,
                            real_name = real_name)

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);",
                    (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);",
                    (login, password_hash, real_name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login = login)


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login, ))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT * FROM articles
            WHERE user_id = %s
            ORDER BY is_favorite DESC, id DESC;
        """, (user_id, ))
    else:
        cur.execute("""
            SELECT * FROM articles
            WHERE user_id = ?
            ORDER BY is_favorite DESC, id DESC;
        """, (user_id, ))

    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles = articles)

@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))  # "on" или None
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        return render_template(
            'lab5/create_article.html',
            error='Тема и текст статьи не могут быть пустыми',
            title=title,
            article_text=article_text,
            is_favorite=is_favorite,
            is_public=is_public
        )

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) "
            "VALUES (%s, %s, %s, %s, %s);",
            (user_id, title, article_text, is_favorite, is_public)
        )
    else:
        cur.execute(
            "INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) "
            "VALUES (?, ?, ?, ?, ?);",
            (user_id, title, article_text, int(is_favorite), int(is_public))
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # текущий пользователь
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()

    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/')

    user_id = user_row["id"]

    # статья этого пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template(
            'lab5/edit_article.html',
            title=article['title'],
            article_text=article['article_text'],
            is_favorite=article['is_favorite'],
            is_public=article['is_public']
        )

    # POST: сохраняем изменения
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        db_close(conn, cur)
        return render_template(
            'lab5/edit_article.html',
            error='Тема и текст статьи не могут быть пустыми',
            title=title,
            article_text=article_text,
            is_favorite=is_favorite,
            is_public=is_public
        )

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles "
            "SET title=%s, article_text=%s, is_favorite=%s, is_public=%s "
            "WHERE id=%s AND user_id=%s;",
            (title, article_text, is_favorite, is_public, article_id, user_id)
        )
    else:
        cur.execute(
            "UPDATE articles "
            "SET title=?, article_text=?, is_favorite=?, is_public=? "
            "WHERE id=? AND user_id=?;",
            (title, article_text, int(is_favorite), int(is_public), article_id, user_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Находим текущего пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()

    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/')

    user_id = user_row["id"]

    # Удаляем ТОЛЬКО свою статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "DELETE FROM articles WHERE id=%s AND user_id=%s;",
            (article_id, user_id)
        )
    else:
        cur.execute(
            "DELETE FROM articles WHERE id=? AND user_id=?;",
            (article_id, user_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')


@lab5.route('/lab5/users')
def users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/users.html', users=users, login=login)


@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login, real_name FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id, login, real_name FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return redirect('/lab5/')

    user_id = user['id']
    current_name = user['real_name']

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/profile.html', login=login, real_name=current_name)

    # POST
    real_name = request.form.get('real_name', '').strip()
    password = request.form.get('password', '').strip()
    password_confirm = request.form.get('password_confirm', '').strip()

    error = None

    if not real_name:
        error = 'Имя не может быть пустым'

    if not error and (password or password_confirm):
        if password != password_confirm:
            error = 'Пароль и подтверждение не совпадают'

    if error:
        db_close(conn, cur)
        return render_template('lab5/profile.html',
                            login=login,
                            real_name=real_name,
                            error=error)

    # Обновляем имя и, при необходимости, пароль
    if password:
        password_hash = generate_password_hash(password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s, password=%s WHERE id=%s;",
                        (real_name, password_hash, user_id))
        else:
            cur.execute("UPDATE users SET real_name=?, password=? WHERE id=?;",
                        (real_name, password_hash, user_id))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE id=%s;",
                        (real_name, user_id))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE id=?;",
                        (real_name, user_id))

    db_close(conn, cur)
    return redirect('/lab5/')


@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.id, a.title, a.article_text, a.is_favorite, u.login, u.real_name
            FROM articles a
            JOIN users u ON a.user_id = u.id
            WHERE a.is_public = TRUE
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)
    else:
        cur.execute("""
            SELECT a.id, a.title, a.article_text, a.is_favorite, u.login, u.real_name
            FROM articles a
            JOIN users u ON a.user_id = u.id
            WHERE a.is_public = 1
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/public_articles.html',
                        articles=articles,
                        login=session.get('login'))


@lab5.route('/lab5/toggle_favorite/<int:article_id>', methods=['POST'])
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # текущий пользователь
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()
    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/')

    user_id = user_row["id"]

    # переключаем только свою статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET is_favorite = NOT is_favorite "
            "WHERE id=%s AND user_id=%s;",
            (article_id, user_id)
        )
    else:
        cur.execute(
            "UPDATE articles SET is_favorite = CASE is_favorite WHEN 1 THEN 0 ELSE 1 END "
            "WHERE id=? AND user_id=?;",
            (article_id, user_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/toggle_public/<int:article_id>', methods=['POST'])
def toggle_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # текущий пользователь
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_row = cur.fetchone()
    if not user_row:
        db_close(conn, cur)
        return redirect('/lab5/')

    user_id = user_row["id"]

    # переключаем только свою статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET is_public = NOT is_public "
            "WHERE id=%s AND user_id=%s;",
            (article_id, user_id)
        )
    else:
        cur.execute(
            "UPDATE articles SET is_public = CASE is_public WHEN 1 THEN 0 ELSE 1 END "
            "WHERE id=? AND user_id=?;",
            (article_id, user_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')