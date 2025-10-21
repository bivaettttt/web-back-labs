from flask import Blueprint, request, redirect, abort, render_template

lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {'name': 'роза', 'price': 150},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 40}
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return render_template('flower.html', flower=flower_list[flower_id], flower_id=flower_id)


@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return redirect('/lab2/flowers')


@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    return 'Вы не задали имя цветка и цену', 400


@lab2.route('/lab2/flowers')
def all_flowers():
    return render_template('flowers.html', flowers=flower_list)


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/flowers')


@lab2.route('/lab2/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower_list.pop(flower_id)
        return redirect('/lab2/flowers')


@lab2.route('/lab2/add_flower_form')
def add_flower_form():
    name = request.args.get('name')
    price = request.args.get('price')
    if name and price:
        flower_list.append({'name': name, 'price': int(price)})
    return redirect('/lab2/flowers')


@lab2.route('/lab2/example')
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


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b, 
                        sum=a+b, 
                        diff=a-b, 
                        mult=a*b, 
                        div=a/b if b != 0 else 'Ошибка: деление на ноль', 
                        pow=a**b)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
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


@lab2.route('/lab2/books')
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


@lab2.route('/lab2/cars')
def cars_list():
    return render_template('cars.html', cars = cars)