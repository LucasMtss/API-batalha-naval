from flask import Flask 
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

@socketio.on('jogar')
def handleMessage(jogador):
    print('sala criada para '+jogador)
    emit('jogar', f'você está coectado na sala: ${jogador}')
    send("SALA CRIADA!!! " + jogador)

if __name__ == '__main__':
	socketio.run(app)