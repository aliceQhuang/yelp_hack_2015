from flask import Flask
from flask import request
import json
from pymongo import MongoClient
from validation.schema import add_person_schema
from jsonschema import validate
from jsonschema import ValidationError


app = Flask(__name__)
client = MongoClient('10.255.55.16', 27017)
db = client.dex
people_collection = db.people
evolutions_collection = db.evolutions


def get_everyone():
    with open('huehue.json', 'r') as f:
        return json.loads(f.read())


def _verify_key(key):
    return key in ('name', 'id', 'region', 'type', 'ability', 'evolution.1', 'evolution.2', 'evolution.3', 'evolution.4', 'move.1', 'move.2', 'move.3', 'move.4')


@app.after_request
def add_header(response):
    # For ajax
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/count')
def hit_counter():
    with open('hit_count', 'r') as f:
        web_count = int(f.read())
    web_count = web_count + 1
    return str(web_count)


@app.route('/everyone')
def everyone():
    results = people_collection.find()
    response = {}
    for result in results:
        del result['_id']
        identifier = result['id']
        response[identifier] = result
    return json.dumps(response, sort_keys=True)


@app.route('/person/<name>')
def person(name):
    response = people_collection.find_one({'id': name})
    del response['_id']
    return json.dumps(response)


@app.route('/add', methods=['POST'])
def add():
    body = request.get_json(force=True)
    print json.dumps(body)
    if not body:
        return json.dumps({
            'error': 'no data'
        })

    try:
        validate(body, add_person_schema)
        people_collection.insert(body)
        del body['_id']
        return json.dumps(body)
    except ValidationError:
        return json.dumps({
            'error': 'invalid schema'
        })


@app.route('/update/<identifier>')
def update(identifier):
    params = request.args
    adjusted_params = {}
    for k, v in params.iteritems():
        if _verify_key(k):
            adjusted_params[k] = v
    for k, v in adjusted_params.iteritems():
        if v:
            people_collection.update({'id': identifier}, {'$set': {k: v}})
        else:
            people_collection.update({'id': identifier}, {'$unset': {k: v}})
    return 'asd'


@app.route('/evo')
def evo_chain():
    results = evolutions_collection.find()
    response = {}
    for result in results:
        del result['_id']
        identifier = result['id']
        response[identifier] = result
    return json.dumps(response, sort_keys=True)


@app.route('/reset')
def reset():
    people_collection.drop()
    everyone = get_everyone()
    people_collection.insert(everyone.values())

    evolutions_collection.drop()
    evo_links = {}
    for identifier, person in everyone.iteritems():
        evos = person['evolution']
        for k, v in evos.iteritems():
            if v == identifier:
                fuck = evo_links.get(identifier, {'after': [], 'before': []})
                # find after
                evolution = str(int(k) + 1)
                if evolution in evos:
                    person_id = evos[evolution]
                    fuck['after'].append(person_id)
                # find before
                evolution = str(int(k) - 1)
                if evolution in evos:
                    person_id = evos[evolution]
                    fuck['before'].append(person_id)
                evo_links[identifier] = fuck
    formatted_links = []
    for identifier, links in evo_links.iteritems():
        formatted_links.append({
            'id': identifier,
            'after': links['after'],
            'before': links['before'],
        })
    evolutions_collection.insert(formatted_links)

    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19000, debug=True)
