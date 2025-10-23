from flask import Flask, request, jsonify
from models.User import User

app = Flask(__name__)
users = []


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

    # Возвращаем данные пользователя
    return jsonify({
        'id': user.id,
        'login': user.login,
        'phone': user.phone
        # Не возвращаем пароль из соображений безопасности!
    }), 200

if __name__ == '__main__':
    app.run(debug=True)