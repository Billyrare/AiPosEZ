import sqlite3
from flask import Flask, request, jsonify, redirect, url_for
import logging
from flask_cors import CORS  # Импорт CORS
from authlib.integrations.flask_client import OAuth
# import jwt
# import os
#
# app = Flask(__name__)
# CORS(app, supports_credentials=True)
# oauth = OAuth(app)
#
# # Настройка провайдеров OAuth
# oauth.register(
#     name='google',
#     client_id=os.getenv('545892399450-ngh15078ol0o9ktng2kps06f0gop1cin.apps.googleusercontent.com'),
#     client_secret=os.getenv('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'),
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     refresh_token_url=None,
#     redirect_uri='http://127.0.0.1:5000/authorize/google',
#     client_kwargs={'scope': 'openid email profile'}
# )
#
#
# def load_secret_key(file_path):
#     with open(file_path, 'r') as file:
#         return file.read().strip()
#
#
# SECRET_KEY = load_secret_key('C:/Users/ASUS/Desktop/уроки/АиПОСиЗИ/lab8/secret_key.txt')
#
#
# # Загрузка секретного ключа из файла или переменной окружения
# # SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_default_secret_key')
#
#
# @app.route('/login/<provider>')
# def login(provider):
#     redirect_uri = url_for('authorize', provider=provider, _external=True)
#     return oauth.create_client(provider).authorize_redirect(redirect_uri)
#
#
# @app.route('/authorize/<provider>')
# def authorize(provider):
#     token = oauth.create_client(provider).authorize_access_token()
#     # Здесь можно добавить логику сохранения информации пользователя
#     jwt_token = jwt.encode({'user_info': token['userinfo']}, SECRET_KEY, algorithm='HS256')
#     return redirect(f'http://127.0.0.1:5000/?token={jwt_token}')  # URL фронтенда


# Настройки логирования
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')


app = Flask(__name__)
CORS(app, supports_credentials=True)


# Обработчик для получения всех записей
@app.route('/all', methods=['GET'])
def get_all():
    try:
        conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cars')
        items = cursor.fetchall()
        conn.close()
        result = [{'car_id': item[0], 'manufacturer': item[1], 'model_name': item[2], 'engine_capacity': item[3],
                   'owner_name': item[4], 'year': item[5], 'color': item[6], 'check_in': item[7]} for item in items]
        return jsonify(result)
    except Exception as e:
        logging.error(f'Ошибка при запросе /all: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка в сервере'}), 500


# Обработчик для добавления новой записи
@app.route('/post', methods=['POST'])
def post_item():
    try:
        data = request.get_json()
        name = data.get('manufacturer')
        conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Cars (manufacturer, model_name, engine_capacity, owner_name, year, color, check_in) VALUES ('
            '?,?,?,?,?,?,?)',
            (data.get('manufacturer'), data.get('model_name'), data.get('engine_capacity'), data.get('owner_name'),
             data.get('year'), data.get('color'), data.get('check_in')))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Данные успешны внесены в базу!'})
    except Exception as e:
        logging.error(f'Ошибка при внесении данных: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка в сервере'}), 500


# Обработчик для получения определенной записи
@app.route('/get/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Cars WHERE car_id=?', (item_id,))
        item = cursor.fetchone()
        conn.close()
        if item is None:
            return jsonify({'message': 'Объект не найдет'}), 404
        return jsonify({'car_id': item[0], 'manufacturer': item[1], 'model_name': item[2], 'engine_capacity': item[3],
                        'owner_name': item[4], 'year': item[5], 'color': item[6], 'check_in': item[7]})
    except Exception as e:
        logging.error(f'Ошибка при получении данных: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка в сервере'}), 500


# Обработчик для обновления записи
@app.route('/update/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json()
        conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE Cars SET manufacturer=?, model_name=?, engine_capacity=?, owner_name=?, year=?, color=?, check_in=? WHERE car_id=?',
            (data.get('manufacturer'), data.get('model_name'), data.get('engine_capacity'), data.get('owner_name'),
             data.get('year'), data.get('color'), data.get('check_in'), item_id))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Запись успешно обновлена!'})
    except Exception as e:
        logging.error(f'Ошибка при обновлении данных: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка в сервере'}), 500


# Обработчик для удаления записи
@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Cars WHERE car_id=?', (item_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Запись успешно удалена!'})
    except Exception as e:
        logging.error(f'Ошибка при удалении данных: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка в сервере'}), 500


if __name__ == '__main__':
    app.run(debug=True)
