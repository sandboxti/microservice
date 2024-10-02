from flask import Flask, request, jsonify
import memcache
import os

app = Flask(__name__)

memcached_host = os.getenv('MEMCACHED_HOST', '127.0.0.1')
memcached_port = 11211
mc = memcache.Client([f'{memcached_host}:{memcached_port}'], debug=0)

@app.route('/users', methods=['GET'])
def get_users():
    users = mc.get('users') or []
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    
    if username:
        users = mc.get('users') or []
        users.append(username)
        mc.set('users', users)
        return jsonify({'message': 'Usuario agregado con éxito'}), 200
    return jsonify({'message': 'Falta el nombre del usuario'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
