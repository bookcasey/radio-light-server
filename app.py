from flask import Flask, abort, make_response, jsonify, request
from flask.ext.cors import CORS, cross_origin

from pi_switch import RCSwitchSender

app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

sender = RCSwitchSender()
sender.enableTransmit(0) # use WiringPi pin 0

# Python for ease of RasPi
# real db next

# less important: adding dynamically
# less important: websockets

switches = [
    {
        'id': 1,
        'name': 'Outlet One',
        'codes' : {
            'on': 4281795,
            'off': 4281660
        },
        'state': False
    },
    {
        'id': 2,
        'name': 'Outlet Two',
        'codes' : {
            'on': 4281795,
            'off': 4281804
        },
        'state': False
    },
    {
        'id': 3,
        'name': 'Outlet Three',
        'codes' : {
            'on': 4282115,
            'off': 4282124
        },
        'state': False
    },
    {
        'id': 4,
        'name': 'Outlet Four',
        'codes' : {
            'on': 4283651,
            'off': 4289804
        },
        'state': False
    },
    {
        'id': 5,
        'name': 'Outlet Five',
        'codes' : {
            'on': 4289795,
            'off': 4289804
        },
        'state': False
    }
]

@app.route('/', methods=['GET'])
@cross_origin()
def redirect_to_index():
    return make_response(open('public/index.html').read())

@app.route('/api/switches', methods=['GET'])
@cross_origin()
def get_switches():
    return jsonify({'switches': switches})

@app.route('/api/switches/<int:switch_id>', methods=['GET'])
@cross_origin()
def get_switch(switch_id):
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if len(switch) == 0:
        abort(404)
    return jsonify({'switches': switch[0]})

@app.route('/api/switches/<int:switch_id>', methods=['PUT'])
@cross_origin()
def update_switch(switch_id):
    #return "ECHO: POST\n"
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if len(switch) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'state' in request.json and type(request.json['state']) is not bool:
        abort(400)
    switch[0]['state'] = request.json.get('state', switch[0]['state'])
    if switch[0]['codes']['on']:
        sender.sendDecimal(69, 24)
    if switch[0]['codes']['on'] == False:
        sender.sendDecimal(69, 24)
    return jsonify({'switches': switch[0]})

@app.errorhandler(404)
@cross_origin()
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
