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
random_shit = db.information


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
    web_count_doc = random_shit.find_one({'property': 'hit_count'})
    if not web_count_doc:
        random_shit.insert({
            'property': 'hit_count',
            'value': 1
        })
        web_count = 1
    else:
        web_count = web_count_doc['value']
    web_count = web_count + 1
    random_shit.update({'property': 'hit_count'}, {'$set': {'value': web_count}})
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
        evos = person['evolution'].values()
        # make sure the person is in their own chain
        if identifier not in evos:
            continue
        if len(evos) > 1:
            for i in range(0, len(evos)):
                if i-1 >= 0:
                    fuck = evo_links.get(evos[i], {'after': set(), 'before': set()})
                    fuck['before'].add(evos[i-1])
                    evo_links[evos[i]] = fuck
                if i+1 < len(evos):
                    fuck = evo_links.get(evos[i], {'after': set(), 'before': set()})
                    fuck['after'].add(evos[i+1])
                    evo_links[evos[i]] = fuck
    formatted_links = []
    for identifier, links in evo_links.iteritems():
        formatted_links.append({
            'id': identifier,
            'before': sorted(links['before']),
            'after': sorted(links['after']),
        })
    evolutions_collection.insert(formatted_links)

    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19000, debug=True)
