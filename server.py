from flask import Flask, request
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}

@socketio.on('connect')
def connect():
    print('Cliente conectado')

@socketio.on('disconnect')
def disconnect_request():
    user = connected_users.pop(request.sid, None)
    print('Cliente desconectado:', user)

@socketio.on('username')
def receive_username(username):
    original_username = username
    count = 1
    while username in connected_users.values():
        username = f"{original_username}{count}"
        count += 1
    connected_users[request.sid] = username

@socketio.on('message')
def handle_message(data):
    username = connected_users[request.sid]
    for sid, user in connected_users.items():
        emit('response', f'{username}: {data}', room=sid)

if __name__ == '__main__':
    socketio.run(app)
