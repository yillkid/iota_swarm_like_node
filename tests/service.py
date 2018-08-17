#!/usr/bin/env python3
import time
import json

import urllib.request
import urllib.parse

def generate_address(url):
    data = {
        "command": "generate_address"
    }

    print("Generating an unused address ... ")
    start = time.time()
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req, json.dumps(data).encode('utf-8'))
    end = time.time()
    print("Response ... %s" % (str(response.read())))
    
    elapsed = end - start
    print("Duration: %s seconds" % (str(elapsed)))

def get_tips(url, command_type):
    data = {
        "command": "get_tips",
        "type": command_type,
    }

    print("Getting tips ...")
    start = time.time()
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req, json.dumps(data).encode('utf-8'))
    end = time.time()
    print("Response ... %s" % (str(response.read())))

    elapsed = end - start
    print("Duration: %s seconds" % (str(elapsed)))

def send_transfer(url, command_type, tag, message, address, value):
    data = {
        'command': 'send_transfer',
        'tag': tag,
        'message': message,
        'address': address,
        'value': value,
        'tips_type': command_type,
        'debug': 1
    }

    print("Send send transfer command ... ")
    start = time.time()
    req = urllib.request.Request(url)
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req, json.dumps(data).encode('utf-8'))
    end = time.time()
    print("Response ... %s" % (str(response.read())))

    elapsed = end - start
    print("Duration: %s seconds" % (str(elapsed)))
