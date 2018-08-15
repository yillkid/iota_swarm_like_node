#import time
import json
from swarm_node import get_tips, send_transfer, \
    find_transactions_by_address

def load(data):
    result = ""
    request_data = json.loads(data)

    if request_data['command'] == "new_claim":
        result = bundle_hash = new_claim(data)
    elif request_data['command'] == "get_all_claims_in_channel":
        result = bundle_hash = get_all_claims_in_channel(data)

    return result

def new_claim(data):
    data = json.loads(data)

    # Get tips
    dict_tips = get_tips(1)

    # Prepare transaction
    address = data['channel'].ljust(81,'9')
    tag = data['uuid'] + "C"

    # Set output transaction
    response = send_transfer(tag, json.dumps(data), address, 0, dict_tips, debug=0)

    return str(response)

def get_all_claims_in_channel(data):
    data = json.loads(data)
    address = data['channel'].ljust(81,'9')
    print "Hello address = " + str(address)
    
    result = find_transactions_by_address(address)
    return result
