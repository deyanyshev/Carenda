from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory

from models.Car import Car
from models.Motorcycle import Motorcycle
from models.User import User

app = Flask(__name__)
CORS(app, origins=['http://localhost:4200'])
users = []
transports = []

def initialize_transports():
    # АВТОМОБИЛИ
    transports.extend([
        # СЕДАНЫ (5-местные)
        Car(
            brand = "Toyota",
            model = "Camry",
            year = 2022,
            img="1.jpg",
            price_per_hour = 500,
            seats = 5,
            transmission = "automatic"
        ),
        Car(
            brand = "BMW",
            model = "5 Series",
            year=2023,
            img="2.jpg",
            price_per_hour=900,
            seats=5,
            transmission="automatic"
        ),

        # ВНЕДОРОЖНИКИ (7 местные)

        Car(
            brand="Toyota",
            model="Land Cruiser",
            year=2022,
            img="3.jpg",
            price_per_hour=1000,
            seats=7,
            transmission="automatic"
        ),

        # КУПЕ (2-местные)
        Car(
            brand="Mercedes-Benz",
            model="C-Class Coupe",
            year=2023,
            img="4.jpg",
            price_per_hour=1200,
            seats=2,
            transmission="automatic"
        ),

        Car(
            brand="Porsche",
            model="911 Carrera",
            year=2023,
            img="5.jpg",
            price_per_hour=2000,
            seats=2,
            transmission="automatic"
        ),

        # МИНИВЭНЫ (7-местные)
        Car(
            brand="Toyota",
            model="Alphard",
            year=2023,
            img="6.jpg",
            price_per_hour=1100,
            seats=7,
            transmission="automatic"
        )
    ])

    # МОТОЦИКЛЫ
    transports.extend([
        # СПОРТИВНЫЕ
        Motorcycle(
            brand="Yamaha",
            model="YZF-R6",
            year=2021,
            img="7.jpg",
            price_per_hour=600,
            bike_type="sport",
            engine_volume=600,
            has_helmet=True
        ),
        Motorcycle(
            brand="Honda",
            model="CBR 1000RR",
            year=2023,
            img="8.jpg",
            price_per_hour=900,
            bike_type="sport",
            engine_volume=1000,
            has_helmet=False
        ),
        Motorcycle(
            brand="Kawasaki",
            model="Ninja 400",
            year=2022,
            img="9.jpg",
            price_per_hour=450,
            bike_type="sport",
            engine_volume=400,
            has_helmet=True
        ),

        # КРУИЗЕРЫ
        Motorcycle(
            brand="Harley-Davidson",
            model="Street 750",
            year=2020,
            img="10.jpg",
            price_per_hour=700,
            bike_type="cruiser",
            engine_volume=750,
            has_helmet=True
        ),
        Motorcycle(
            brand="Indian",
            model="Chief",
            year=2023,
            img="11.jpg",
            price_per_hour=800,
            bike_type="cruiser",
            engine_volume=1800,
            has_helmet=True
        ),

        # ТУРИНГОВЫЕ
        Motorcycle(
            brand="BMW",
            model="R 1250 GS",
            year=2023,
            img="12.jpg",
            price_per_hour=850,
            bike_type="touring",
            engine_volume=1250,
            has_helmet=True
        )
    ])





@app.route('/register', methods=['POST'])
def register():
    data = request.json

    if not data.get('login') or not data.get('password') or not data.get('phone'):
        return jsonify({'error': 'Need login, password and phone'}), 400

    if any(user.login == data['login'] for user in users):
        return jsonify({'error': 'User exists'}), 400
    users.append(User(len(users) + 1, data['login'], data['password'], data['phone']))

    return jsonify({'id': users[-1].id}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data.get('login') or not data.get('password'):
        return jsonify({'error': 'Need login and password'}), 400

    user = next((u for u in users if u.login == data['login'] and u.password == data['password']), None)

    if not user:
        return jsonify({'error': 'Invalid login or password'}), 401

    return jsonify({'id': user.id}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Ищем пользователя по ID
    user = next((u for u in users if u.id == user_id), None)

    # Если пользователь не найден - возвращаем ошибку
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Преобразуем историю аренд в словари
    rental_history_data = []
    for rental in user.rental_history:
        rental_data = {
            'transport_id': rental.transport.transport_id,
            'start_time': rental.start_date.isoformat() if rental.start_date else None,
            'end_time': rental.end_date.isoformat() if rental.end_date else None
        }
        rental_history_data.append(rental_data)

    # Преобразуем текущую аренду в словарь
    current_rental_data = None
    if user.current_rental:
        current_rental_data = {
            'transport_id': user.current_rental.transport.transport_id,
            'start_time': user.current_rental.start_date.isoformat() if user.current_rental.start_date else None
        }

    # Возвращаем данные пользователя
    return jsonify({
        'id': user.id,
        'login': user.login,
        'phone': user.phone,
        'current_rental': current_rental_data,  # Добавляем текущую аренду
        'rental_history': rental_history_data   # Добавляем историю аренд
        # Не возвращаем пароль из соображений безопасности!
    }), 200


@app.route('/transports', methods=['GET'])
def get_transports():
    """Получить список всего транспорта"""

    # Преобразуем объекты транспорта в словари для JSON
    transports_data = []
    for transport in transports:
        # Базовые данные для всех типов транспорта
        transport_data = {
            'id': transport.transport_id,
            'brand': transport.brand,
            'model': transport.model,
            'year': transport.year,
            'img': transport.img,
            'price_per_hour': transport.price_per_hour,
            'is_available': transport.is_available,
        }

        # Добавляем специфичные поля для автомобилей
        if type(transport).__name__ == 'Car':
            transport_data['seats'] = transport.seats
            transport_data['transmission'] = transport.transmission

        # Добавляем специфичные поля для мотоциклов
        else:
            transport_data['bike_type'] = transport.bike_type
            transport_data['engine_volume'] = transport.engine_volume
            transport_data['has_helmet'] = transport.has_helmet

        transports_data.append(transport_data)

    return jsonify(transports_data), 200


@app.route('/transports/<transport_id>', methods=['GET'])
def get_transport(transport_id):
    """Получить конкретный транспорт по ID"""

    # Ищем транспорт по ID
    transport = next((t for t in transports if t.transport_id == transport_id), None)

    # Если транспорт не найден - возвращаем ошибку
    if not transport:
        return jsonify({'error': 'Transport not found'}), 404

    # Базовые данные для всех типов транспорта
    transport_data = {
        'id': transport.transport_id,
        'brand': transport.brand,
        'model': transport.model,
        'year': transport.year,
        'img': transport.img,
        'price_per_hour': transport.price_per_hour,
        'is_available': transport.is_available,
        'type': transport.get_type()
    }

    # Добавляем специфичные поля для автомобилей
    if transport.get_type() == 'car':
        transport_data['seats'] = transport.seats
        transport_data['transmission'] = transport.transmission

    # Добавляем специфичные поля для мотоциклов
    elif transport.get_type() == 'motorcycle':
        transport_data['bike_type'] = transport.bike_type
        transport_data['engine_volume'] = transport.engine_volume
        transport_data['has_helmet'] = transport.has_helmet

    return jsonify(transport_data), 200


@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('photo', filename)



@app.route('/transports/<transport_id>', methods=['GET'])
def get_transport(transport_id):
    """Получить конкретный транспорт по ID"""

    # Ищем транспорт по ID
    transport = next((t for t in transports if t.transport_id == transport_id), None)

    # Если транспорт не найден - возвращаем ошибку
    if not transport:
        return jsonify({'error': 'Transport not found'}), 404

    # Базовые данные для всех типов транспорта
    transport_data = {
        'id': transport.transport_id,
        'brand': transport.brand,
        'model': transport.model,
        'year': transport.year,
        'img': transport.img,
        'price_per_hour': transport.price_per_hour,
        'is_available': transport.is_available,
        'type': transport.get_type()
    }

    # Добавляем специфичные поля для автомобилей
    if transport.get_type() == 'car':
        transport_data['seats'] = transport.seats
        transport_data['transmission'] = transport.transmission

    # Добавляем специфичные поля для мотоциклов
    elif transport.get_type() == 'motorcycle':
        transport_data['bike_type'] = transport.bike_type
        transport_data['engine_volume'] = transport.engine_volume
        transport_data['has_helmet'] = transport.has_helmet

    return jsonify(transport_data), 200



@app.route('/transports/<transport_id>/rent', methods=['PATCH'])
def rent_transport(transport_id):
    """Начать аренду транспорта"""
    data = request.json

    # Проверяем обязательное поле user_id
    if not data.get('user_id'):
        return jsonify({'error': 'Need user_id'}), 400

    # Ищем транспорт и пользователя
    transport = next((t for t in transports if t.transport_id == transport_id), None)
    user = next((u for u in users if u.id == data['user_id']), None)

    # Проверяем что нашли и транспорт и пользователя
    if not transport:
        return jsonify({'error': 'Transport not found'}), 404
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Проверяем доступность транспорта
    if not transport.is_available:
        return jsonify({'error': 'Transport is already rented'}), 400

    # Проверяем что у пользователя нет активной аренды
    if user.current_rental:
        return jsonify({'error': 'User already has active rental'}), 400

    # Начинаем аренду
    transport.is_available = False
    user.current_rental = {
        'transport_id': transport_id,
        'start_time': datetime.now().isoformat()
    }

    return  200


if __name__ == '__main__':
    initialize_transports()
    app.run(debug=True)