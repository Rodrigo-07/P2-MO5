from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)

CORS(app)

# Cada vez que uma dessas rotas receber uma requisição, armazenar o horário do servidor e a requisição realizada em uma lista com essas informações.

db_log = TinyDB('db_log.json', indent=4)


@app.before_request
def log_request():
    print(request.endpoint)
    if request.method == "GET" and request.endpoint == 'ping':
        db_log.insert({'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'requisicao': request.method, 'endpoint': request.endpoint, 'parametros': request.args})
    elif request.method == "POST" and request.endpoint == 'echo':
        db_log.insert({'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'requisicao': request.method, 'endpoint': request.endpoint, 'dados': request.json})

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/ping')
def ping():
    return jsonify({'resposta': 'pong'})


# # Endpoint para receber dados de um  e retornar esses dados em formato JSON.
@app.route('/echo', methods=['POST'])
def echo():
    mensagem = request.json['dados']

    # Return the message as JSON
    return jsonify({'resposta': mensagem})

# Endpoint para retornar a lista de logs armazenados.
@app.route('/dash', methods=['GET'])
def dash():
    logs = db_log.all()
    return render_template('dashboard.html', logs=logs)

# Endpoint  retornar mídia sobre os dados armazenados.
@app.route('/info', methods=['GET'])
def info():
    logs = db_log.all()
    mensagem = f'<p>{logs}</p>'
    return mensagem


if __name__ == '__main__':
    app.run()

