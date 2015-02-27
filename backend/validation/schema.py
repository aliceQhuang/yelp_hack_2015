add_person_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'id': {'type': 'string'},
        'type': {'type': 'string'},
        'region': {'type': 'string'},
        'ability': {'type': 'string'},
        'evolution': {
            'type': 'object',
            'properties': {
                '1': {'type': 'string'},
                '2': {'type': 'string'},
                '3': {'type': 'string'}
            },
            'required': ['1']
        },
        'move': {
            'type': 'object',
            'properties': {
                '1': {'type': 'string'},
                '2': {'type': 'string'},
                '3': {'type': 'string'},
                '4': {'type': 'string'}
            },
            'required': ['1']
        }
    },
    'required': [
        'name',
        'id',
        'type',
        'region',
        'ability',
        'evolution',
        'move'
    ]
}
