import time

import requests
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

sala = dict()


def createUser(name):
    response = requests.post('http://127.0.0.1:5001/users', {"nome": name})
    return response.json()


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

# Verifica se a sala está cheia
def verify_room():
    for i in sala:
        if sala[i]["size"] == 1:
            return i


# Salva o board do usuario
@socketio.on("board")
def send_board(data):
    room = data["room"]
    user = data["user"]
    board = data["board"]
    sala[room][user] = board
    emit("send_board", sala[room], room=room)


def joinRoom(room, user, num=1):
    join_room(room)
    sala[room]["size"] = num
    sala[room][f'{user}'] = []
    print(sala[room])
    emit("room_message", f"Your room: {room}", room=room)
    if (num == 2):
        time.sleep(2.5)  # deixar esse sleep por causa do front
        emit("room_message", "Sala cheia", room=room)

# Inicia ou adiciona um novo usuario na sala
@socketio.on("join")
def on_join(data):
    room = verify_room()
    user = data["user"]
    if room == None:
        room = data["room"]
        sala[room] = {"jogador1": user}
        joinRoom(room, user)
    else:
        sala[room]["jogador2"] = user
        joinRoom(room, user, 2)


if __name__ == '__main__':
    socketio.run(app, debug=True)
