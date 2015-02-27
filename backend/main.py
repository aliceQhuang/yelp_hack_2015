from flask import Flask
import json


app = Flask(__name__)


def get_everyone():
    with open('huehue.json', 'r') as f:
        return json.loads(f.read())


@app.route('/everyone')
def everyone():
    return json.dumps(get_everyone())


@app.route('/person/<name>')
def person(name):
    everyone = get_everyone()
    return json.dumps(everyone[name])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19000)
