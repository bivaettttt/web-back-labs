from flask import Blueprint, url_for, request, redirect
import datetime
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1")
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <a href="/">Вернуться на главную страницу</a>
        
        <h2>Список роутов</h2>
        <ol>
            <li><a href="/">Главная страница (/)</a></li>
            <li><a href="/index">Главная страница (/index)</a></li>
            <li><a href="/lab1/web">Web страница</a></li>
            <li><a href="/lab1/author">Автор</a></li>
            <li><a href="/lab1/image">Изображение</a></li>
            <li><a href="/lab1/counter">Счетчик</a></li>
            <li><a href="/lab1/cl_counter">Сброс счетчика</a></li>
            <li><a href="/lab1/info">Информация</a></li>
            <li><a href="/lab1/created">Создано</a></li>
            <li><a href="/400">Ошибка 400</a></li>
            <li><a href="/401">Ошибка 401</a></li>
            <li><a href="/402">Ошибка 402</a></li>
            <li><a href="/403">Ошибка 403</a></li>
            <li><a href="/405">Ошибка 405</a></li>
            <li><a href="/418">Ошибка 418</a></li>
            <li><a href="/error500">Тест ошибки 500</a></li>
        </ol>
    </body>
</html>
'''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Надршин Тимур Ринатович"
    group = "ФБИ-32"
    faculty = "ФБ"
    
    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""


@lab1.route('/lab1/image')
def image():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    
    html_content = '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''
    
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Language': 'ru',
        'X-Developer': 'Timur Nadrshin',
        'X-Image-Source': 'Nature Gallery',
    }
    
    return html_content, 200, headers


count = 0


@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <br>
        <a href="/lab1/cl_counter">Сбросить счетчик</a>
    </body>
</html>
'''


@lab1.route('/lab1/cl_counter')
def cl_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счетчик был очищен</h1>
        <a href='/lab1/counter'>Перейти к счетчику</a>
    </body>
</html>
'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201