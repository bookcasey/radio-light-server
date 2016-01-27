from flask import Flask
from flask import abort
from flask import make_response
from flask import jsonify



import simplejson as json

app = Flask(__name__)

switches = [
    {
        'id': 1,
        'codes' : {
            'on': 12345,
            'off': 12346
        },
        'state': False
    },
    {
        'id': 2,
        'codes' : {
            'on': 23456,
            'off': 23457
        },
        'state': False
    }
]

@app.route('/api/switches', methods=['GET'])
def get_switches():
    return jsonify({'switches': switches})

@app.route('/api/switches/<int:switch_id>', methods=['GET'])
def get_switch(switch_id):
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if len(switch) == 0:
        abort(404)
    return jsonify({'switches': switch[0]})

@app.route('/api/switches/<int:switch_id>', methods=['PUT'])
def update_task(task_id):
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'state' in request.json and type(request.json['state']) is not bool:
        abort(400)
    switch[0]['state'] = request.json.get('state', switch[0]['done'])
    return jsonify({'switches': switch[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# less important: adding dynamically

if __name__ == '__main__':
    app.run(debug=True)
