from flask import Flask
import json


app = Flask(__name__)


@app.route('/everyone')
def poop():
    with open('huehue.json', 'r') as f:
        return f.read()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19000)
