from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age = 5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user = user, age = age, sex = sex, errors = errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чертный чай - 80 рублей, зеленый - 70 рублей.
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара - на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price = price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price = price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    text_align = request.args.get('text_align')

    if color or bg_color or font_size or text_align:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if text_align:
            resp.set_cookie('text_align', text_align)
        return resp

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    text_align = request.cookies.get('text_align')

    resp = make_response(render_template('lab3/settings.html', 
                                        color=color, 
                                        bg_color=bg_color, 
                                        font_size=font_size,
                                        text_align=text_align))
    return resp


@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket.html')


@lab3.route('/lab3/ticket_result')
def ticket_result():
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    errors = {}

    if not fio:
        errors['fio'] = 'Заполните поле!'
    if not shelf:
        errors['shelf'] = 'Выберите полку!'
    if not linen:
        errors['linen'] = 'Выберите вариант!'
    if not baggage:
        errors['baggage'] = 'Выберите вариант!'
    if not age:
        errors['age'] = 'Заполните поле!'
    elif not age.isdigit() or int(age) < 1 or int(age) > 120:
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Заполните поле!'
    if not destination:
        errors['destination'] = 'Заполните поле!'
    if not date:
        errors['date'] = 'Заполните поле!'
    if not insurance:
        errors['insurance'] = 'Выберите вариант!'

    if errors:
        return render_template('lab3/ticket.html', 
                            errors=errors,
                            fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                            age=age, departure=departure, destination=destination,
                            date=date, insurance=insurance)

    age_int = int(age)

    # Расчет стоимости
    if age_int < 18:
        ticket_type = "Детский билет"
        price = 700
    else:
        ticket_type = "Взрослый билет"
        price = 1000

    if shelf in ['lower', 'lower_side']:
        price += 100

    if linen == 'yes':
        price += 75

    if baggage == 'yes':
        price += 250

    if insurance == 'yes':
        price += 150

    return render_template('lab3/ticket_result.html', 
                        fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                        age=age, departure=departure, destination=destination,
                        date=date, insurance=insurance, ticket_type=ticket_type,
                        price=price)


@lab3.route('/lab3/settings_clear')
def settings_clear():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('text_align')
    return resp


# Список товаров (смартфоны)
PRODUCTS = [
    {'name': 'iPhone 15 Pro', 'price': 120000, 'brand': 'Apple', 'color': 'Титановый', 'storage': '256GB'},
    {'name': 'Samsung Galaxy S24', 'price': 80000, 'brand': 'Samsung', 'color': 'Черный', 'storage': '128GB'},
    {'name': 'Xiaomi 13', 'price': 45000, 'brand': 'Xiaomi', 'color': 'Белый', 'storage': '256GB'},
    {'name': 'Google Pixel 8', 'price': 60000, 'brand': 'Google', 'color': 'Серый', 'storage': '128GB'},
    {'name': 'OnePlus 11', 'price': 55000, 'brand': 'OnePlus', 'color': 'Зеленый', 'storage': '256GB'},
    {'name': 'Realme GT 3', 'price': 35000, 'brand': 'Realme', 'color': 'Синий', 'storage': '128GB'},
    {'name': 'iPhone 14', 'price': 70000, 'brand': 'Apple', 'color': 'Фиолетовый', 'storage': '128GB'},
    {'name': 'Samsung A54', 'price': 30000, 'brand': 'Samsung', 'color': 'Графитовый', 'storage': '128GB'},
    {'name': 'Xiaomi Redmi Note 13', 'price': 25000, 'brand': 'Xiaomi', 'color': 'Голубой', 'storage': '256GB'},
    {'name': 'Google Pixel 7a', 'price': 40000, 'brand': 'Google', 'color': 'Коралловый', 'storage': '128GB'},
    {'name': 'Nothing Phone 2', 'price': 50000, 'brand': 'Nothing', 'color': 'Белый', 'storage': '256GB'},
    {'name': 'Asus ROG Phone 7', 'price': 90000, 'brand': 'Asus', 'color': 'Черный', 'storage': '512GB'},
    {'name': 'Sony Xperia 1 V', 'price': 95000, 'brand': 'Sony', 'color': 'Пурпурный', 'storage': '256GB'},
    {'name': 'Huawei P60 Pro', 'price': 65000, 'brand': 'Huawei', 'color': 'Золотой', 'storage': '256GB'},
    {'name': 'Motorola Edge 40', 'price': 35000, 'brand': 'Motorola', 'color': 'Небесный', 'storage': '256GB'},
    {'name': 'Vivo X90', 'price': 55000, 'brand': 'Vivo', 'color': 'Красный', 'storage': '256GB'},
    {'name': 'Oppo Find X6', 'price': 60000, 'brand': 'Oppo', 'color': 'Черный', 'storage': '256GB'},
    {'name': 'iPhone SE', 'price': 40000, 'brand': 'Apple', 'color': 'Красный', 'storage': '64GB'},
    {'name': 'Samsung Z Flip5', 'price': 110000, 'brand': 'Samsung', 'color': 'Сиреневый', 'storage': '256GB'},
    {'name': 'Xiaomi Poco F5', 'price': 28000, 'brand': 'Xiaomi', 'color': 'Черный', 'storage': '256GB'}
]

@lab3.route('/lab3/products')
def products():
    # Получаем цены из куки или вычисляем
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    # Вычисляем мин и макс цены из всех товаров
    all_prices = [product['price'] for product in PRODUCTS]
    min_price_all = min(all_prices)
    max_price_all = max(all_prices)
    
    # Получаем параметры поиска
    min_price_search = request.args.get('min_price')
    max_price_search = request.args.get('max_price')
    reset = request.args.get('reset')
    
    errors = {}
    
    # Если нажата кнопка сброс
    if reset:
        resp = make_response(redirect('/lab3/products'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    # Если есть параметры поиска - валидируем
    if min_price_search is not None or max_price_search is not None:
        # Проверяем минимальную цену (если не пустая)
        if min_price_search and min_price_search != '':
            if not min_price_search.isdigit():
                errors['min_price'] = 'Цена должна быть числом!'
            elif int(min_price_search) < 0:
                errors['min_price'] = 'Цена не может быть отрицательной!'
        
        # Проверяем максимальную цену (если не пустая)
        if max_price_search and max_price_search != '':
            if not max_price_search.isdigit():
                errors['max_price'] = 'Цена должна быть числом!'
            elif int(max_price_search) < 0:
                errors['max_price'] = 'Цена не может быть отрицательной!'
        
        # Если нет ошибок - обрабатываем поиск
        if not errors:
            # Автоматически исправляем если min > max
            if min_price_search and max_price_search and min_price_search.isdigit() and max_price_search.isdigit():
                min_val = int(min_price_search)
                max_val = int(max_price_search)
                if min_val > max_val:
                    # Меняем поля местами
                    min_price_search, max_price_search = max_price_search, min_price_search
            
            resp = make_response(redirect('/lab3/products'))
            if min_price_search:
                resp.set_cookie('min_price', min_price_search)
            if max_price_search:
                resp.set_cookie('max_price', max_price_search)
            return resp
    
    # Используем значения из куки для фильтрации
    min_price = min_price_cookie
    max_price = max_price_cookie
    
    # Фильтруем товары
    filtered_products = []
    for product in PRODUCTS:
        price = product['price']
        price_match = True
        
        if min_price and min_price.isdigit():
            if price < int(min_price):
                price_match = False
        
        if max_price and max_price.isdigit() and price_match:
            if price > int(max_price):
                price_match = False
        
        if price_match:
            filtered_products.append(product)
    
    return render_template('lab3/products.html',
                        products=filtered_products,
                        min_price=min_price_search or min_price,
                        max_price=max_price_search or max_price,
                        min_price_all=min_price_all,
                        max_price_all=max_price_all,
                        products_count=len(filtered_products),
                        all_products_count=len(PRODUCTS),
                        errors=errors)