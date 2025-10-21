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