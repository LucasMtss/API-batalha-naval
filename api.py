from flask import Flask
from functions import createBattleshipGame

app = Flask(__name__)

@app.route('/')
def root():
  return "<h1>API com Flask</h1>"

@app.route('/gerar-campo')
def generateBattlefield():
  return {
    "status": 200,
    "payload": {
      "matriz": createBattleshipGame()
    }
    }

app.run(debug=True)