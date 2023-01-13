import threading
import time

import requests
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

sala = dict()
disconectedsSockets = []
HOST = 'http://127.0.0.1:5002'

# faz uma requisição para a api de gerar um board


def gen_board():
    response = requests.get(f'{HOST}/gerar-campo')
    return response.json()

#Testado
def createUser(name):
    response = requests.post(f'{HOST}/users', {"nome": name})
    return response.json()


@socketio.on('chat')
def chat(data):
    emit("receiver-msg", data["data"], room=data["room"])


@socketio.on('exit')
def chat(id):
    delete_room_or_player(id)

# gera um board para o usuário


@socketio.on('generate_board')
def generate_board(data):
    response = gen_board()
    board = response["payload"]["matriz"]
    id = data["id"]
    room = data["room"]
    resp = {
        "board": board,
        "id": id
    }
    emit("resp_gen_board", resp, room=room)


# Verifica se a sala está cheia
def verify_room():
    for i in sala:
        if sala[i]["size"] == 1:
            return i


# Salva o board do usuario
@socketio.on("board")
def send_board(data):
    room = data["room"]
    data_board = get_player(room, data["id"])
    board = data["board"]
    data_board["board"] = board
    emit("send_board", sala[room], room=room)
    time.sleep(1)
    emit("get_board", sala[room], room=room)

# altera um board de acordo com as posiçoes passadas


@socketio.on("alter_board")
def send_board(data):
    id = data["id"]
    room = data["room"]
    x = data["x"]
    y = data["y"]
    current_player = get_player(room, id)
    player = get_adversary(room, id)
    if player["board"][x][y] == '0':
        player["board"][x][y] = 'Q'
        current_player["myturn"] = False
        player["myturn"] = True
        sala[room]["acertou"] = False
    else:
        player["board"][x][y] = 'W'
        player["placar"] = player["placar"]+1
        current_player["myturn"] = True
        player["myturn"] = False
        sala[room]["acertou"] = True
        player["acertos"] = player["acertos"] + 1
        if player["acertos"] == 19:
            player["ganhou"] = True
            current_player["ganhou"] = False
    player["cliques"] = player["cliques"] + 1
    emit("send_board", sala[room], room=room)

# Verifica se um usuario se desconectou de uma sala


@socketio.on("disconnect")
def disconect():
    disconectedsSockets.append(request.sid)
    delete_room_or_player(request.sid)
    remove()

# verifica se tem usuarios desconectados no array
# se tiver vai remover todos


@socketio.on("connection")
def connection():
    print('Connected: '+request.sid)
    remove()


def joinRoom(room, num=1):
    join_room(room)
    sala[room]["size"] = num
    emit("id_room", f"Your room: {room}", room=room)
    print(room)
    print(sala[room])
    if (num == 2):
        emit("room_message", "Sala cheia", room=room)

# Inicia ou adiciona um novo usuario na sala


@socketio.on("join")
def on_join(data):
    time.sleep(1)
    room = verify_room()
    username = data["username"]
    if username != None:
        createUser(username)
    if room == None:
        room = data["room"]
        sala[room] = {"size": 0}
        sala[room]["jogador1"] = {
            "name": username, "id": request.sid, "placar": 0, "myturn": True, "cliques": 0, "acertos": 0, "ganhou": -1}
        joinRoom(room)
    else:
        sala[room]["jogador2"] = {"name": username,
                                  "id": request.sid, "placar": 0, "myturn": False, "cliques": 0, "acertos": 0, "ganhou": -1}
        
        joinRoom(room, 2)

# Pega os dados do jogador pelo id dele


def get_player(room, id):
    if sala[room]["jogador1"]["id"] == id:
        return sala[room]["jogador1"]
    else:
        return sala[room]["jogador2"]

# Pega o board do adversario


def get_adversary(room, id):
    if sala[room]["jogador1"]["id"] == id:
        return sala[room]["jogador2"]
    else:
        return sala[room]["jogador1"]

# Deleta um jogador ou uma sala


def delete_room_or_player(id):
    try:
        for idx, dictionary in enumerate(sala):
            if sala[dictionary]["jogador1"]["id"] == id or sala[dictionary]["jogador2"]["id"] == id:
                del sala[dictionary]
                emit("disconected", "Sala excluida!", room=dictionary)
    except:
        print("O tamanho mudou!")


def remove():
    if len(disconectedsSockets) > 0:
        for i in disconectedsSockets:
            delete_room_or_player(i)
            disconectedsSockets.remove(i)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
