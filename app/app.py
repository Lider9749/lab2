from flask import Flask, render_template, request, make_response
import re

app = Flask(__name__)

def format_phone(phone):
    # Удаляем все символы кроме цифр
    digits = ''.join(re.findall(r'\d', phone))
    
    # Если номер начинается с 7 или 8 и содержит 11 цифр, форматируем его
    if len(digits) == 11 and digits[0] in ['7', '8']:
        return f"8-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    # Если номер содержит 10 цифр, добавляем 8 и форматируем
    elif len(digits) == 10:
        return f"8-{digits[0:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:]}"
    return None

def validate_phone(phone):
    # Проверяем на недопустимые символы
    if not re.match(r'^[0-9()+\-\s.]+$', phone):
        return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
    
    # Подсчитываем количество цифр
    digits = ''.join(re.findall(r'\d', phone))
    
    # Проверяем длину
    if phone.startswith('+7') or phone.startswith('8'):
        if len(digits) != 11:
            return "Недопустимый ввод. Неверное количество цифр."
    elif len(digits) != 10:
        return "Недопустимый ввод. Неверное количество цифр."
    
    return None

@app.route('/')
def index():
    return render_template('request_data.html')

@app.route('/headers')
def headers():
    return render_template('request_data.html', headers=dict(request.headers))

@app.route('/cookies')
def cookies():
    response = make_response(render_template('request_data.html', cookies=request.cookies))
    # Устанавливаем тестовую cookie
    response.set_cookie('test_cookie', 'cookie_value')
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('login.html', 
                             form_data=request.form,
                             show_data=True)
    return render_template('login.html', show_data=False)

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error = None
    formatted_phone = None
    
    if request.method == 'POST':
        phone_number = request.form.get('phone', '')
        error = validate_phone(phone_number)
        if not error:
            formatted_phone = format_phone(phone_number)
            
    return render_template('phone.html', 
                         error=error, 
                         formatted_phone=formatted_phone)

if __name__ == '__main__':
    app.run(debug=True) 