from flask import Flask, url_for, request
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

app = Flask(__name__)

app.secret_key = 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)

access_log = []


@app.before_request
def log_requests():
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    log_entry = f"{access_date} - IP: {client_ip} - URL: {requested_url}"
    access_log.append(log_entry)


@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    
    return '''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body {
                font-family: 'Arial';
                background: linear-gradient(135deg, white 0%, black 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                color: white;
            }
            .container {
                text-align: center;
                background: black;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px #002;
                max-width: 900px;
                margin: 0 auto;
            }
            h1 {
                font-size: 50pt;
                margin: 0;
                text-shadow: 2px 2px 4px #002;
            }
            .cat-image {
                max-width: 700px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .home-button {
                display: inline-block;
                padding: 12px 30px;
                background: white;
                color: black;
                text-decoration: none;
                border-radius: 25px;
                font-weight: bold;
                transition: 0.3s;
                margin: 20px 0;
                border: 2px solid transparent;
            }
            .home-button:hover {
                color: white;
                background: black;
                border-color: white;
                transform: translateY(-2px);
            }
            .cat-404 {
                font-size: 14pt;
                margin: 20px 0;
                color: white;
                font-weight: bold;
            }
            .log-container {
                margin-top: 30px;
                padding: 20px;
                border-radius: 10px;
                text-align: left;
            }
            .log-container h3 {
                color: royalblue;
                border-bottom: 1px solid lightblue;
                padding-bottom: 10px;
            }
            .log-list {
                max-height: 300px;
                overflow-y: auto;
                font-family: monospace;
                font-size: 12px;
                padding: 10px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>404 NOT FOUND</h1>
            
            <img src="''' + url_for("static", filename="404.jpg") + '''" class="cat-image" alt="Ошибка 404">
                
            <div class="cat-404">
                О КАК... Страницы нет!
            </div>
            
            <a href="/" class="home-button">На главную страницу</a>
            
            <div class="log-container">
                <h3>Информация о текущем запросе:</h3>
                <p><strong>IP-адрес:</strong> ''' + client_ip + '''</p>
                <p><strong>Дата и время:</strong> ''' + access_date + '''</p>
                <p><strong>Запрошенный URL:</strong> ''' + requested_url + '''</p>
                
                <h3>Полный лог посещений (все адреса):</h3>
                <div class="log-list">
''' + ('<p>Лог пуст</p>' if not access_log else '<ul>' + ''.join([f'<li>{entry}</li>' for entry in access_log]) + '</ul>') + '''
                </div>
                <p><strong>Всего записей в логе:</strong> ''' + str(len(access_log)) + '''</p>
            </div>
        </div>
    </body>
</html>
''', 404


@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>Произошла непредвиденная ошибка на сервере.</p>
        <p>Попробуйте обновить страницу или вернуться позже.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500


@app.route('/error500')
def cause_error():
    result = 10 / 0
    return "Эта строка никогда не выполнится"


@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
            <hr>
        </header>
        
        <main>
            <ol>
                <li><a href="/lab1/">Первая лабораторная</a></li>
                <li><a href="/lab2/">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвёртая лабораторная</a></li>
            </ol>
        </main>
        
        <footer>
            <hr>
            &copy; Надршин Тимур Ринатович, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>
'''