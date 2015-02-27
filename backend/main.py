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


def _verify_key(key):
    return key in ('name', 'id', 'region', 'type', 'ability', 'evolution.1', 'evolution.2', 'evolution.3', 'move.1', 'move.2', 'move.3', 'move.4')


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
    return json.dumps(response, sort_keys=True)


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
    del body['_id']
    return json.dumps(body)


@app.route('/update/<identifier>')
def update(identifier):
    params = request.args
    adjusted_params = {}
    for k, v in params.iteritems():
        if _verify_key(k):
            adjusted_params[k] = v
    for k, v in adjusted_params.iteritems():
        if v:
            people.update({'id': identifier}, {'$set': {k: v}})
        else:
            people.update({'id': identifier}, {'$unset': {k: v}})
    return 'asd'


@app.route('/reset')
def reset():
    people.drop()
    everyone = get_everyone()
    people.insert(everyone.values())
    results = people.find()
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19000, debug=True)
