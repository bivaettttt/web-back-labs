from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
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


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    if not film.get('description'):
        return jsonify({'description': 'Описание не должно быть пустым'}), 400

    films.append(film)
    return jsonify(film), 201


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()

    if not film.get('description'):
        return jsonify({'description': 'Описание не должно быть пустым'}), 400

    films[id] = film
    return films[id]