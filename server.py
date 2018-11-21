#!/usr/bin/env python
import json
from flask import Flask, request
from flask_cors import CORS
from config import *

from swarm_node import send_transfer, get_tips, generate_address
from extensions.tangleid import main as extension_tangleid
from utils import IotaJSONEncoder

app = Flask(__name__)
CORS(app)

@app.route('/')
def swarm_node_info():
    response = {
        'status': 'SUCCESS',
        'data': 'Hello I am a swarm node.'
    }

    return json.dumps(response)


@app.route('/', methods=['POST'])
def execute_api():
    request_data = request.get_data()
    print("Get request data ... %s" % (str(request_data)))

    request_command = json.loads(request_data)

    if request_command['command'] == "generate_address":
        address_result = generate_address()
        result = json.dumps(address_result, cls=IotaJSONEncoder)

    elif request_command['command'] == "get_tips":
        tips_result = get_tips(int(request_command['type']))
        result = json.dumps(tips_result, cls=IotaJSONEncoder)

    elif request_command['command'] == "send_transfer":
        if 'debug' not in request_command:
            debug = 0
        else:
            debug = int(request_command['debug'])

        dict_tips = get_tips(int(request_command['tips_type']))
        result = send_transfer(
            request_command['tag'], request_command['message'], request_command['address'], int(
                request_command['value']), dict_tips, debug)
    else:
        result = extension_tangleid.load(request_data)

    print("Result ... %s" % (str(result)))

    return result

if __name__ == "__main__":
    app.run(port=PORT, threaded=True)
