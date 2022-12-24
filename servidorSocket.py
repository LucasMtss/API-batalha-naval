from flask import Flask 
from flask_socketio import SocketIO, send, emit
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

sala = []

def createUser(name):
    response = requests.post('http://127.0.0.1:5001/users', {"nome": name})
    return response.json()


@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('entrar_sala')
def handleMessage(playerName):
    print('sala criada para '+playerName)

    createUserResponse = createUser(playerName)
    emit('entrar_sala', {'mensagem':'você está coectado na sala '+playerName, 'response': createUserResponse})

if __name__ == '__main__':
	socketio.run(app)