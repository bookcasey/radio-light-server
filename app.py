from flask import Flask, abort, make_response, jsonify, request
from flask.ext.cors import CORS, cross_origin

from pi_switch import RCSwitchSender

app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

sender = RCSwitchSender()
sender.enableTransmit(0) # use WiringPi pin 0
sender.setPulseLength(181)

# Python for ease of RasPi
# real db next

# less important: adding dynamically
# less important: websockets

switches = [
    {
        'id': 1,
        'name': 'Bedside Lamp',
        'codes' : {
            'on': 4281651,
            'off': 4281660
        },
        'state': False
    },
    {
        'id': 2,
        'name': 'Humidifier',
        'codes' : {
            'on': 4281795,
            'off': 4281804
        },
        'state': False
    },
    {
        'id': 3,
        'name': 'Electric Blanket',
        'codes' : {
            'on': 4282115,
            'off': 4282124
        },
        'state': False
    },
    {
        'id': 4,
        'name': 'Air Filter',
        'codes' : {
            'on': 4283651,
            'off': 4283660
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
    print switch_id
    switch = [switch for switch in switches if switch['id'] == switch_id]
    if len(switch) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'state' in request.json and type(request.json['state']) is not bool:
        abort(400)
    switch[0]['state'] = request.json.get('state', switch[0]['state'])
    print switch[0]['state'] # true/false
    print switch[0]['codes']['on']
    if switch[0]['state']:
        sender.sendDecimal(switch[0]['codes']['on'], 24)
    if switch[0]['state'] == False:
        sender.sendDecimal(switch[0]['codes']['off'], 24)

    return jsonify({'switches': switch[0]})

@app.errorhandler(404)
@cross_origin()
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
