from flask import Flask
from flask import request
import json
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('10.255.55.16', 27017)
db = client.dex
people = db.people


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
    results = people.find()
    response = {}
    for result in results:
        del result['_id']
        identifier = result['id']
        response[identifier] = result
    return json.dumps(response)


@app.route('/person/<name>')
def person(name):
    response = people.find_one({'id': name})
    del response['_id']
    return json.dumps(response)


@app.route('/add', methods=['POST'])
def add():
    body = request.get_json(force=True)
    if body:
        people.insert(body)
    return body


@app.route('/reset')
def reset():
    people.drop()
    everyone = get_everyone()
    people.insert(everyone.values())
    results = people.find()
    for result in results:
        print result
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19000, debug=True)
