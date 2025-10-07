from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

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
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ol>
        </main>
        
        <footer>
            <hr>
            &copy; Надршин Тимур Ринатович, ФБИ-32, 3 курс, 2025
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
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
            <li><a href="/cl_counter">Сброс счетчика</a></li>
            <li><a href="/lab1/info">Информация</a></li>
            <li><a href="/created">Создано</a></li>
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
    
@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route('/lab1/image')
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

@app.route('/lab1/counter')
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
        <a href="/cl_counter">Сбросить счетчик</a>
    </body>
</html>
'''

@app.route('/cl_counter')
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/created")
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

@app.route("/400")
def bad_request():
    return '''
<!doctype html>
<html>
    <head>
        <title>400 Bad Request</title>
    </head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может обработать запрос из-за клиентской ошибки (неправильный синтаксис, неверный запрос и т.д.)</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 400

@app.route("/401")
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 401

@app.route("/402")
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Зарезервировано для будущего использования. Первоначально предназначалось для цифровых платежных систем.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 402

@app.route("/403")
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен, даже при аутентификации.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 403

@app.route("/405")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса не поддерживается для данного ресурса.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 405

@app.route("/418")
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я - чайник. Этот код был введен как первоапрельская шутка в 1998 году.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 418

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
    <body>
        <h1>Цветок №{flower_id}</h1>
        <p>Название: {flower_list[flower_id]}</p>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/add_flower/')
def add_flower_nothing():
    return 'Вы не задали имя цветка', 400

@app.route('/lab2/flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Все цветы</h1>
        <p>Количество цветов: {len(flower_list)}</p>
        <ul>
            <li>{'</li><li>'.join(flower_list)}</li>
        </ul>
        <a href="/lab2/clear_flowers">Очистить список цветов</a>
    </body>
</html>
'''

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name, num, group, course = 'Тимур Надршин', 2, 'ФБИ-32', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                            name = name, num = num, group = group,
                            course = course, fruits = fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b, 
                        sum=a+b, 
                        diff=a-b, 
                        mult=a*b, 
                        div=a/b if b != 0 else 'Ошибка: деление на ноль', 
                        pow=a**b)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

books = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказы', 'pages': 350},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 640}
]

@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books = books)

cars = [
    {'name': 'Toyota Camry', 'image': 'camry.jpg', 'description': 'Надежный седан бизнес-класса'},
    {'name': 'Honda Civic', 'image': 'civic.jpg', 'description': 'Компактный автомобиль с отличной экономией'},
    {'name': 'BMW X5', 'image': 'x5.jpg', 'description': 'Премиальный кроссовер от немецкого бренда'},
    {'name': 'Mercedes-Benz S-Class', 'image': 'sclass.jpg', 'description': 'Флагманский седан класса люкс'},
    {'name': 'Audi A4', 'image': 'a4.jpg', 'description': 'Спортивный седан премиум-класса'},
    {'name': 'Ford Mustang', 'image': 'mustang.jpg', 'description': 'Легендарный американский мускулкар'},
    {'name': 'Volkswagen Golf', 'image': 'golf.jpg', 'description': 'Компактный хэтчбек с богатой историей'},
    {'name': 'Hyundai Solaris', 'image': 'solaris.jpg', 'description': 'Популярный седан для города'},
    {'name': 'Kia Rio', 'image': 'rio.jpg', 'description': 'Стильный и экономичный седан'},
    {'name': 'Nissan Qashqai', 'image': 'qashqai.jpg', 'description': 'Компактный кроссовер для семьи'},
    {'name': 'Mercedes-Benz G-Class', 'image': 'gclass.jpg', 'description': 'Легендарный внедорожник класса люкс'},
    {'name': 'BMW M5', 'image': 'm5.jpg', 'description': 'Высокопроизводительный спортивный седан'},
    {'name': 'Subaru Outback', 'image': 'outback.jpg', 'description': 'Универсал повышенной проходимости'},
    {'name': 'Mazda CX-5', 'image': 'cx5.jpg', 'description': 'Стильный кроссовер с отличной управляемостью'},
    {'name': 'Volvo XC90', 'image': 'xc90.jpg', 'description': 'Безопасный и комфортный SUV'},
    {'name': 'Porsche 911', 'image': '911.jpg', 'description': 'Легендарный спортивный автомобиль'},
    {'name': 'Jeep Wrangler', 'image': 'wrangler.jpg', 'description': 'Внедорожник для настоящих приключений'},
    {'name': 'Tesla Model 3', 'image': 'model3.jpg', 'description': 'Электрический седан будущего'},
    {'name': 'Land Rover Defender', 'image': 'defender.jpg', 'description': 'Легендарный внедорожник'},
    {'name': 'Ferrari 488', 'image': 'ferrari.jpg', 'description': 'Итальянский суперкар'}
]

@app.route('/lab2/cars')
def cars_list():
    return render_template('cars.html', cars = cars)