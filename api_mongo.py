from textwrap import indent
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json

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
    "placar": None
  }
  return mongo.db.salas.insert_one(room).inserted_id

def update_room(id, data):
  print('\n\nUPDATE', id, data)
  mongo.db.salas.update_one(
    {'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': data}
  )
        
def insert_user_in_room(userId):
  rooms = mongo.db.salas.find()
  rooms = json_util.dumps(list(rooms), indent=2)
  if rooms == '[]':
    roomId = create_room()
    roomData = {
      "jogador_um": userId,
      "jogador_dois": None,
      "tabuleiro_jogador_um": None,
      "tabuleiro_jogador_dois": None,
      "placar": None
    }
    print('\n\nROOM DATA', roomData)
    update_room(roomId, roomData)
    return roomId
  else:
    roomsJson = json.loads(rooms)
    if roomsJson[0]['jogador_um'] == None:
      roomsJson[0]['jogador_um'] = userId
    else:
      roomsJson[0]['jogador_dois'] = userId
    roomData = {
      "jogador_um": roomsJson[0]['jogador_um'],
      "jogador_dois": roomsJson[0]['jogador_dois'],
      "tabuleiro_jogador_um": roomsJson[0]['tabuleiro_jogador_um'],
      "tabuleiro_jogador_dois": roomsJson[0]['tabuleiro_jogador_dois'],
      "placar": roomsJson[0]['placar']
    }
    update_room(roomsJson[0]['_id'], roomData)
    return roomsJson[0]['_id']['$oid']

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    nome = request.json['nome']
    if nome:
        id = mongo.db.usuarios.insert_one({'nome': nome}).inserted_id
        response = jsonify({
            '_id': str(id),
            'nome': nome,
        })
        insert_user_in_room(id)
        response.status_code = 201
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
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
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
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)