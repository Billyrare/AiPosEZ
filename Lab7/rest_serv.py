from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Обработчик для получения всех записей
@app.route('/all', methods=['GET'])
def get_all():
    conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Cars')
    items = cursor.fetchall()
    conn.close()
    result = [{'car_id': item[0], 'manufacturer': item[1], 'model_name': item[2],'engine_capacity': item[3],'owner_name': item[3],'year': item[4],'color': item[5],'check_in': item[6]} for item in items]
    return jsonify(result)

# Обработчик для добавления новой записи
@app.route('/post', methods=['POST'])
def post_item():
    data = request.get_json()
    name = data.get('manufacturer')
    conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Cars (manufacturer) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item added successfully!'})

# Обработчик для получения определенной записи
@app.route('/get/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = sqlite3.connect('C:/Users/ASUS/Documents/build-crud_app-Desktop_Qt_5_12_12_MinGW_64_bit-Debug/cars.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Cars WHERE car_id=?', (item_id,))
    item = cursor.fetchone()
    conn.close()
    if item is None:
        return jsonify({'message': 'Item not found'}), 404
    return jsonify({'car_id': item[0], 'manufacturer': item[1]})

# Запускаем сервер
if __name__ == '__main__':
    app.run(debug=True)
