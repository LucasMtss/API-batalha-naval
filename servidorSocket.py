from flask import Flask 
from flask_socketio import SocketIO, send, emit
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

rooms = []

def createUser(name):
    response = requests.post('http://127.0.0.1:5001/users', {"nome": name})
    return response.json()


def saveRoom(newRoom):
    print('\n\nNOVA SALA', newRoom, '\n\n')
    if(newRoom['pode_iniciar'] == True):
        print('PASSOU')
        emit('iniciar_partida', {
            'mensagem':
                'A sala '+newRoom['_id']['$oid'] +' iniciou a partida para os jogadores: ' + newRoom['jogador_um']['nome']+ ' e '+ newRoom['jogador_dois']['nome'],
            'response': {
                'jogador_um': newRoom['jogador_um'],
                'jogador_dois': newRoom['jogador_dois'],
                'sala': newRoom['_id'],
            }
        }, broadcast=True)
    for index, room in enumerate(rooms):
        if room['_id']['$oid'] == newRoom ['_id']['$oid']:
            rooms.pop(index)
            rooms.append(newRoom)
            return
    rooms.append(newRoom)
   


@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('entrar_sala',)
def handleMessage(playerName):
    print('sala criada para '+playerName)

    createUserResponse = createUser(playerName)
    print("\n\n", type(createUserResponse), "\n\n")
    saveRoom(createUserResponse['payload'])
    emit('entrar_sala', {'mensagem':'você está coectado na sala '+playerName, 'response': createUserResponse})

if __name__ == '__main__':
	socketio.run(app)