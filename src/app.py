from flask import Flask, request, render_template
from flask_cors import CORS
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)

CORS(app)

# Cada vez que uma dessas rotas receber uma requisição, armazenar o horário do servidor e a requisição realizada em uma lista com essas informações.

db_log = TinyDB('db_log.json', indent=4)

@app.before_request
def log_request():
    if request.method == "GET":
        db_log.insert({'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'requisicao': request.method, 'endpoint': request.endpoint, 'parametros': request.args})
    elif request.method == "POST":
        db_log.insert({'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'requisicao': request.method, 'endpoint': request.endpoint, 'dados': request.json})

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return {'resposta': 'pong'}


# Endpoint para receber dados de um formulário e retornar esses dados em formato JSON.
@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    return data

@app.route('/dash', methods=['GET'])
def dash():
    logs = db_log.all()
    return render_template('dashboard.html', logs=logs)

# Endpoint Para obter as informações para a construção da página, criar a rota '/info', que deve retornar mídia (HTML) sobre os dados armazenados.
@app.route('/info', methods=['GET'])



if __name__ == '__main__':
    app.run()

