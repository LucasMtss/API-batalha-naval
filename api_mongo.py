from textwrap import indent
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
from functions import createBattleshipGame

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/batalha_naval'

mongo = PyMongo(app)

def create_room():
  room={
    "jogador_um": None,
    "jogador_dois": None,
    "tabuleiro_jogador_um": None,
    "tabuleiro_jogador_dois": None,
    "placar": None,
    "pode_iniciar": False
  }
  return mongo.db.salas.insert_one(room).inserted_id

def update_room(id, data):
  mongo.db.salas.update_one(
    {'_id': ObjectId(id)}, {'$set': data}
  )
  response = mongo.db.salas.find_one({'_id': ObjectId(id)})
  
  return json.loads(json_util.dumps(response))

def getIdOfPlayer(player):
  if player == None:
    return None
  else:
    try:
      id = player['$oid']
      return ObjectId(id)
    except:
      return ObjectId(player)

def creatRoomAndInsertPlayer(userId):
  roomId = create_room()
  roomData = {
    "jogador_um": userId,
    "jogador_dois": None,
    "tabuleiro_jogador_um": None,
    "tabuleiro_jogador_dois": None,
    "placar": None,
    "pode_iniciar": False
  }
  update_room(roomId, roomData)
  return getRoomData(roomId)
  
def checkIfRoomIsFull(room):
  return room['jogador_um'] != None and room['jogador_dois'] != None

def getAvaibleRoom(rooms):
  for room in rooms:
    if checkIfRoomIsFull(room) == False:
      return room
  return None

def insertPlayerInRoom(room, userId):
  if room['jogador_um'] == None:
    room['jogador_um'] = ObjectId(userId)
  else:
    room['jogador_dois'] = ObjectId(userId)
  roomData = {
    "jogador_um": getIdOfPlayer(room['jogador_um']),
    "jogador_dois": getIdOfPlayer(room['jogador_dois']),
    "tabuleiro_jogador_um": room['tabuleiro_jogador_um'],
    "tabuleiro_jogador_dois": room['tabuleiro_jogador_dois'],
    "placar": room['placar'],
    "pode_iniciar": False
  }
  update_room(room['_id']['$oid'], roomData)
  return getRoomData(room['_id']['$oid'])
        
def insert_user_in_room(userId):
  rooms = mongo.db.salas.find()
  rooms = json_util.dumps(list(rooms), indent=2)
  # Não existem salas cadastradas
  if rooms == '[]':
    return creatRoomAndInsertPlayer(userId)
  else:
    roomsJson = json.loads(rooms)
    # Verifica se existe alguma sala com pelo menos uma vaga
    selectedRoom = getAvaibleRoom(roomsJson)
    
    # Caso não existir, cria uma sala nova e insere o jogador
    if selectedRoom == None:
      return creatRoomAndInsertPlayer(userId)
    # Caso exista uma sala vazia, insere o jogador nela
    response = insertPlayerInRoom(selectedRoom, userId)
    if checkIfRoomIsFull(selectedRoom):
      return initGame(selectedRoom)
    return(response)

def initGame(room):
  score = {
    "jogador_um": {
      "jogador": getUserData(getIdOfPlayer(room['jogador_um'])),
      "pontos": 0
    },
    "jogador_dois": {
      "jogador": getUserData(getIdOfPlayer(room['jogador_dois'])),
      "pontos": 0
    },
  }

  battleshipPlayerOne = {
    "tabuleiro": createBattleshipGame(),
    "navios_destruidos": []
  }

  battleshipPlayerTwo = {
    "tabuleiro": createBattleshipGame(),
    "navios_destruidos": []
  }

  roomData = {
    "jogador_um": getIdOfPlayer(room['jogador_um']),
    "jogador_dois": getIdOfPlayer(room['jogador_dois']),
    "tabuleiro_jogador_um": battleshipPlayerOne,
    "tabuleiro_jogador_dois": battleshipPlayerTwo,
    "placar": score,
    "pode_iniciar": True,
  }

  response = update_room(room['_id']['$oid'], roomData)
  response['jogador_um'] = getUserData(getIdOfPlayer(room['jogador_um']))
  response['jogador_dois'] = getUserData(getIdOfPlayer(room['jogador_dois']))
  return response

def getRoomData(roomId):
  response = mongo.db.salas.find_one({'_id': ObjectId(roomId)})
  roomData = json.loads(json_util.dumps(response))
  roomData['jogador_um'] = getUserData(getIdOfPlayer(roomData['jogador_um']))
  roomData['jogador_dois'] = getUserData(getIdOfPlayer(roomData['jogador_dois']))
  return roomData

def getUserData(userId):
  response = mongo.db.usuarios.find_one({'_id': ObjectId(userId)})
  return json.loads(json_util.dumps(response))

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    nome = request.form.get('nome')
    if nome:
        id = mongo.db.usuarios.insert_one({'nome': nome}).inserted_id
        response = {
          "payload": insert_user_in_room(id),
          "status_code": 201
        }
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.usuarios.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id) })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def   not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5001)