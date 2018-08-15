#!/usr/bin/env python
import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser

from swarm_node import send_transfer, get_tips, generate_address
from extensions.loader import call_plugin

PORT = 8000


class RequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        response = {
            'status': 'SUCCESS',
            'data': 'Hello I am a swarm node.'
        }

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response))

    def do_POST(self):

        request_path = self.path

        request_headers = self.headers
        content_length = request_headers.get("Content-length")
        length = int(content_length) if content_length else 0
        request_data = self.rfile.read(length)
        request_data = request_data.decode('utf-8')
        print("Get request data ... %s" % (str(request_data)))

        request_command = json.loads(request_data)
        result = -1

        if 'extension' in request_command:
            result = call_plugin(request_command['extension'], request_command)
        else:
            result = swarm_node_commands(request_command)

        if result == -1:
           print("Invalid request, check 'command' key-value pairs in request data")
        else:
            print("Result ... %s" % (str(result)))

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(str(result).encode('utf-8'))


def http_server():

    print("Listening on localhost: %s" % (str(PORT)))
    server = HTTPServer(('', PORT), RequestHandler)
    server.serve_forever()


def swarm_node_commands(request_command):
    result = -1

    if request_command['command'] == "generate_address":
        result = generate_address()
    elif request_command['command'] == "get_tips":
        result = get_tips(int(request_command['type']))
    elif request_command['command'] == "send_transfer":
        if 'debug' not in request_command:
            debug = 0
        else:
            debug = int(request_command['debug'])

        dict_tips = get_tips(int(request_command['tips_type']))
        result = send_transfer(
            request_command['tag'], request_command['message'], request_command['address'], int(
                request_command['value']), dict_tips, debug)

    return result

http_server()
