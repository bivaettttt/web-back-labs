from lab5 import db_connect, db_close

from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime
import sqlite3

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def main():
    init_films_table()
    return render_template('lab7/index.html')


# начальные данные – только для первичного заполнения БД
initial_films = [
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'title_ru': 'Гарри Поттер и Философский камень',
        'year': 2001,
        'description': 'Юный волшебник Гарри Поттер узнаёт о своём происхождении и поступает \
        в школу магии Хогвартс. Там он сталкивается с тайной Философского камня, \
        а также с проявлениями тёмных сил, стремящихся вернуть своего хозяина.'
    },
    {
        'title': 'John Wick',
        'title_ru': 'Джон Уик',
        'year': 2014,
        'description': 'После смерти жены Джон Уик получает в подарок щенка, \
        который становится его последней связью с дорогим человеком. \
        Когда бандиты убивают собаку и похищают его машину, Джон возвращается \
        в криминальный мир, чтобы отомстить и восстановить справедливость.'
    },
    {
        'title': 'Legend',
        'title_ru': 'Легенда',
        'year': 2015,
        'description': 'Фильм рассказывает историю близнецов Крэй — Реджи и Ронни, \
        двух самых известных гангстеров Лондона 1960-х годов. \
        Они строят собственную криминальную империю, сталкиваясь с насилием, \
        предательством и внутренними демонами.'
    },
    {
        'title': 'The Gentlemen',
        'title_ru': 'Джентльмены',
        'year': 2019,
        'description': 'Американец Микки Пирсон построил прибыльный бизнес по выращиванию \
        марихуаны в Великобритании. Когда он решает продать своё дело, \
        это запускает цепочку интриг, шантажа и криминальных игр между \
        несколькими влиятельными группировками.'
    },
    {
        'title': 'Now You See Me',
        'title_ru': 'Иллюзия обмана',
        'year': 2013,
        'description': 'Команда талантливых иллюзионистов, известных как Четыре Всадника, \
        устраивает публичные шоу, во время которых они совершают дерзкие ограбления. \
        Их преследуют ФБР и Интерпол, но фокусники всегда остаются на шаг впереди.'
    }
]


def init_films_table():
    """Создаём таблицу films и заполняем её начальными данными, если она пустая."""
    conn, cur = db_connect()
    try:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                title_ru TEXT NOT NULL,
                year INTEGER NOT NULL,
                description TEXT NOT NULL
            )
        ''')

        # универсальный подсчёт записей (sqlite / postgres)
        cur.execute('SELECT COUNT(*) AS cnt FROM films')
        row = cur.fetchone()
        if isinstance(row, dict) or hasattr(row, 'keys'):
            count = row['cnt']
        else:
            count = row[0]

        if count == 0:
            use_sqlite = isinstance(conn, sqlite3.Connection)
            ph = '?' if use_sqlite else '%s'

            # задаём id явно (1..N), чтобы не было NULL в Postgres
            for i, f in enumerate(initial_films, start=1):
                cur.execute(
                    f'INSERT INTO films (id, title, title_ru, year, description) '
                    f'VALUES ({ph}, {ph}, {ph}, {ph}, {ph})',
                    (i, f['title'], f['title_ru'], f['year'], f['description'])
                )

        conn.commit()
    finally:
        db_close(conn, cur)


def row_to_film(row):
    """Преобразование строки БД в словарь фильма (sqlite / postgres)."""
    if isinstance(row, dict) or hasattr(row, 'keys'):
        return {
            'id': row['id'],
            'title': row['title'],
            'title_ru': row['title_ru'],
            'year': row['year'],
            'description': row['description'],
        }
    else:
        return {
            'id': row[0],
            'title': row[1],
            'title_ru': row[2],
            'year': row[3],
            'description': row[4],
        }


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    init_films_table()
    conn, cur = db_connect()
    try:
        cur.execute('SELECT id, title, title_ru, year, description FROM films ORDER BY id')
        rows = cur.fetchall()
    finally:
        db_close(conn, cur)
    return jsonify([row_to_film(r) for r in rows])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    init_films_table()
    conn, cur = db_connect()
    try:
        use_sqlite = isinstance(conn, sqlite3.Connection)
        ph = '?' if use_sqlite else '%s'

        cur.execute(
            f'SELECT id, title, title_ru, year, description FROM films WHERE id = {ph}',
            (id,)
        )
        row = cur.fetchone()
    finally:
        db_close(conn, cur)

    if row is None:
        abort(404)

    return row_to_film(row)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    init_films_table()
    conn, cur = db_connect()
    try:
        use_sqlite = isinstance(conn, sqlite3.Connection)
        ph = '?' if use_sqlite else '%s'

        cur.execute(f'DELETE FROM films WHERE id = {ph}', (id,))
        deleted = cur.rowcount
        conn.commit()
    finally:
        db_close(conn, cur)

    if deleted == 0:
        abort(404)

    return '', 204


def validate_film_data(film):
    """Проверки для полей фильма по заданию 15."""
    title_ru = film.get('title_ru', '').strip()
    title = film.get('title', '').strip()
    year_raw = film.get('year', '')
    description = film.get('description', '').strip()

    if title_ru == '':
        return False, {'title_ru': 'Заполните русское название'}

    if title == '' and title_ru == '':
        return False, {'title': 'Должно быть заполнено хотя бы одно название'}

    current_year = datetime.now().year
    try:
        year = int(year_raw)
    except (TypeError, ValueError):
        return False, {'year': 'Год должен быть числом'}

    if year < 1895 or year > current_year:
        return False, {'year': f'Год должен быть от 1895 до {current_year}'}

    if description == '':
        return False, {'description': 'Заполните описание'}
    if len(description) > 2000:
        return False, {'description': 'Описание не должно превышать 2000 символов'}

    if title == '' and title_ru != '':
        title = title_ru

    film['title'] = title
    film['title_ru'] = title_ru
    film['year'] = year
    film['description'] = description

    return True, film


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    init_films_table()
    film = request.get_json()

    ok, result = validate_film_data(film)
    if not ok:
        return result, 400

    conn, cur = db_connect()
    try:
        use_sqlite = isinstance(conn, sqlite3.Connection)
        ph = '?' if use_sqlite else '%s'

        cur.execute(
            f'UPDATE films SET title = {ph}, title_ru = {ph}, year = {ph}, description = {ph} '
            f'WHERE id = {ph}',
            (result['title'], result['title_ru'], result['year'], result['description'], id)
        )
        updated = cur.rowcount
        conn.commit()
    finally:
        db_close(conn, cur)

    if updated == 0:
        abort(404)

    result['id'] = id
    return result, 200


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    init_films_table()
    film = request.get_json()

    ok, result = validate_film_data(film)
    if not ok:
        return result, 400

    conn, cur = db_connect()
    try:
        use_sqlite = isinstance(conn, sqlite3.Connection)
        ph = '?' if use_sqlite else '%s'

        # сами считаем новый id (MAX(id) + 1), чтобы не зависеть от SERIAL/IDENTITY
        cur.execute('SELECT COALESCE(MAX(id), 0) AS max_id FROM films')
        row = cur.fetchone()
        if isinstance(row, dict) or hasattr(row, 'keys'):
            max_id = row['max_id']
        else:
            max_id = row[0]
        new_id = max_id + 1

        cur.execute(
            f'INSERT INTO films (id, title, title_ru, year, description) '
            f'VALUES ({ph}, {ph}, {ph}, {ph}, {ph})',
            (new_id, result['title'], result['title_ru'], result['year'], result['description'])
        )
        conn.commit()
    finally:
        db_close(conn, cur)

    result['id'] = new_id

    return {"id": new_id, "film": result}, 201