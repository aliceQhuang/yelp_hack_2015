from flask import Flask
import json


app = Flask(__name__)


def get_everyone():
    with open('huehue.json', 'r') as f:
        return json.loads(f.read())


@app.after_request
def add_header(response):
    # For ajax
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/everyone')
def everyone():
    return json.dumps(get_everyone())


@app.route('/person/<name>')
def person(name):
    everyone = get_everyone()
    response_body = json.dumps(everyone[name])
    return response_body


@app.route('/add')
def add():
    return 'asd'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19000, debug=True)
