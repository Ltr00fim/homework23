import os
from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def _limit(data, value):
    """ Функция для вывода данных в ограниченном размере """
    i = 0
    for k in data:
        if i > int(value):
            break
        yield k
        i += 1

def _command(data, cmd, value):
    """ Функция, выполняющая команды """
    if cmd == "map":
        return map(lambda x: x.split(" ")[int(value)], data)
    if cmd == "filter":
        return filter(lambda x: value in x, data)
    if cmd == "unique":
        return iter(set(data))
    if cmd == "sort":
        return sorted(data, reverse=False)
    if cmd == "limit":
        return _limit(data, int(value))

def query(data, cmd1: str, cmd2: str, value1: str, value2: int):
    data = _command(data, cmd1, value1)
    data = _command(data, cmd2, value2)
    return data

@app.route("/")
@app.route("/perform_query/")
def perform_query():
    try:
        cmd1 = request.json['cmd1']
        cmd2 = request.json['cmd2']
        value1 = request.json['value1']
        value2 = request.json['value2']
        filename = request.json['filename']
    except Exception as e:
        raise f"<h1>{e}</h1>"

    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        with open (file_path) as f:
            data = '\n'.join(query(f, cmd1, cmd2, value1, value2))
    else:
        raise "<h1>Нет файла</h1>"

    return app.response_class(data, content_type="text/plain")

if __name__ == '__main__':
    app.run(debug=True, host="localhost")
