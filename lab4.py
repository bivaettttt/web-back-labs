from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')

    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum', methods=['GET', 'POST'])
def sum_numbers():
    if request.method == 'POST':
        x1 = request.form.get('x1', '0')
        x2 = request.form.get('x2', '0')

        x1 = int(x1) if x1 != '' else 0
        x2 = int(x2) if x2 != '' else 0

        result = x1 + x2
        return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

    return render_template('lab4/sum.html')


@lab4.route('/lab4/multiply', methods=['GET', 'POST'])
def multiply():
    if request.method == 'POST':
        x1 = request.form.get('x1', '1')
        x2 = request.form.get('x2', '1')

        x1 = int(x1) if x1 != '' else 1
        x2 = int(x2) if x2 != '' else 1

        result = x1 * x2
        return render_template('lab4/multiply.html', x1=x1, x2=x2, result=result)

    return render_template('lab4/multiply.html')


@lab4.route('/lab4/subtract', methods=['GET', 'POST'])
def subtract():
    if request.method == 'POST':
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')

        if x1 == '' or x2 == '':
            return render_template('lab4/subtract.html', error='Оба поля должны быть заполнены!')

        x1 = int(x1)
        x2 = int(x2)
        result = x1 - x2
        return render_template('lab4/subtract.html', x1=x1, x2=x2, result=result)

    return render_template('lab4/subtract.html')


@lab4.route('/lab4/power', methods=['GET', 'POST'])
def power():
    if request.method == 'POST':
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')

        if x1 == '' or x2 == '':
            return render_template('lab4/power.html', error='Оба поля должны быть заполнены!')

        x1 = int(x1)
        x2 = int(x2)

        if x1 == 0 and x2 == 0:
            return render_template('lab4/power.html', error='Оба числа не могут быть равны нулю!')

        result = x1 ** x2
        return render_template('lab4/power.html', x1=x1, x2=x2, result=result)

    return render_template('lab4/power.html')


tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count

    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut':
        # Проверка, чтобы счетчик не ушел в отрицательную область
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        # Проверка, чтобы не превысить максимум 10 деревьев
        if tree_count < 10:
            tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'john9977', 'password': '456', 'name': 'Джон Смит', 'gender': 'male'},
    {'login': 'mary', 'password': '789', 'name': 'Мария Иванова', 'gender': 'female'},
    {'login': 'sophia', 'password': 'qwerty', 'name': 'София Козлова', 'gender': 'female'},
    {'login': 'max2023', 'password': 'password', 'name': 'Максим Сидоров', 'gender': 'male'},
    {'login': 'anna_b', 'password': 'anna123', 'name': 'Анна Белова', 'gender': 'female'},
    {'login': 'dmitry', 'password': 'dima777', 'name': 'Дмитрий Волков', 'gender': 'male'},
    {'login': 'kate88', 'password': 'katya88', 'name': 'Екатерина Морозова', 'gender': 'female'},
    {'login': 'sergey', 'password': 'sergio', 'name': 'Сергей Николаев', 'gender': 'male'},
    {'login': 'olga_s', 'password': 'olga2024', 'name': 'Ольга Семенова', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            # Находим имя и пол пользователя по логину
            for user in users:
                if login == user['login']:
                    name = user['name']
                    gender = user['gender']
                    break
            else:
                name = login
                gender = ''
            return render_template('lab4/login.html', authorized=authorized, name=name, gender=gender)
        else:
            authorized = False
            login = ''
        return render_template('lab4/login.html', authorized=authorized, login=login)

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые значения
    if login == '':
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login)

    if password == '':
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login_value=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login_value=login)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    # Проверка на пустое значение
    if temperature == '':
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    temperature = int(temperature)
    
    # Проверка диапазонов
    if temperature < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    
    if temperature > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    
    # Определение количества снежинок
    if -12 <= temperature <= -9:
        snowflakes = 3
    elif -8 <= temperature <= -5:
        snowflakes = 2
    elif -4 <= temperature <= -1:
        snowflakes = 1
    else:
        snowflakes = 0
    
    return render_template('lab4/fridge.html', 
                        temperature=temperature, 
                        snowflakes=snowflakes, 
                        success=True)


