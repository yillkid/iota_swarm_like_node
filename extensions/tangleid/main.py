import time
import json
from swarm_node import get_tips, send_transfer, \
    find_transactions_by_tag, get_txn_msg, find_transactions_by_address

address = "BXEOYAONFPBGKEUQZDUZZZODHWJDWHEOYY9AENYF9VNLXZHXBOODCOTYXW9MGGINTEJPLK9AGOPTPODVX"


def load(data):
    request_data = json.loads(data)

    if request_data['command'] == "new_claim":
        bundle_hash = new_claim(data)
        return bundle_hash
    elif request_data['command'] == "get_all_claims":
        list_claims = list_all_claims(data)
        return list_claims
    elif request_data['command'] == "get_claim_info":
        result = get_claim_info(data)
        return result
    elif request_data['command'] == "login":
        result = login(data)
        return result
    elif request_data['command'] == "new_user":
        result = new_user(data)
        return result
    elif request_data['command'] == "send_notify":
        result = send_notify(data)
        return result
    elif request_data['command'] == "get_all_notifies":
        result = get_all_notifies(data)
        return result
    elif request_data['command'] == "revoke_claim":
        result = revoke_claim(data)
        return result
    elif request_data['command'] == "get_all_revoke_claims":
        result = get_all_revoke_claims(data)
        return result
    elif request_data['command'] == "new_group":
        result = new_group(data)
        return result
    elif request_data['command'] == "get_all_claims_in_channel":
        result = get_all_claims_in_channel(data)
        return result


def new_claim(data):
    data = json.loads(data)

    # Get tips
    dict_tips = get_tips(0)

    # Set output transaction
    tag = data['uuid'] + "C"
    if 'addr' in data:
        response = send_transfer(tag, json.dumps(data), data['addr'], 0, dict_tips, debug=0)
    else:
        response = send_transfer(tag, json.dumps(data), address, 0, dict_tips, debug=0)

    return str(response)


def list_all_claims(data):
    data = json.loads(data)

    uuid = data['uuid']
    uuid = uuid + "C"

    list_claims = find_transactions_by_tag(uuid)

    if len(list_claims) == 0:
        return []

    list_claims = list_claims['hashes']

    list_output = []
    for obj in list_claims:
        list_output.append(str(obj))

    return str(json.dumps(list_output))


def get_claim_info(data):
    data = json.loads(data)

    txn_hash = data['hash_txn']
    result = get_txn_msg(txn_hash)

    return result


def login(data):
    data = json.loads(data)

    uuid = data['uuid'] + "I"

    list_result = find_transactions_by_tag(uuid)

    return str(list_result)


def new_user(data):
    data = json.loads(data)

    # Get tips
    dict_tips = get_tips(0)

    # Set output transaction
    tag = data['uuid'] + "I"
    response = send_transfer(tag, json.dumps(data), address, 0, dict_tips, debug=0)

    return str(response)


def send_notify(data):
    data = json.loads(data)

    # Get tips
    dict_tips = get_tips(0)

    # Set output transaction
    tag = data['uuid'] + "M"
    response = send_transfer(tag, json.dumps(data), address, 0, dict_tips, debug=0)

    return str(response)


def get_all_notifies(data):
    data = json.loads(data)

    uuid = data['uuid']
    uuid = uuid + "M"

    list_claims = find_transactions_by_tag(uuid)

    if len(list_claims) == 0:
        return []

    list_claims = list_claims['hashes']

    list_output = []
    for obj in list_claims:
        list_output.append(str(obj))

    return str(list_output)


def revoke_claim(data):
    data = json.loads(data)

    # Get tips
    dict_tips = get_tips(0)

    # Set output transaction
    tag = data['uuid'] + "R"
    response = send_transfer(tag, json.dumps(data), address, 0, dict_tips, debug=0)

    return str(response)


def get_all_revoke_claims(data):
    data = json.loads(data)

    uuid = data['uuid']
    uuid = uuid + "R"

    #list_result = api.find_transactions(tags = [uuid])
    list_result = find_transactions_by_tag(uuid)

    return str(list_result)


def new_group(data):
    data = json.loads(data)

    # Get tips
    dict_tips = get_tips(0)

    # Set output transaction
    tag = data['uuid'] + "G"
    response = send_transfer(tag, json.dumps(data), address, 0, dict_tips, debug=0)

    return str(response)

def get_all_claims_in_channel(data):
    data = json.loads(data)

    address = data['channel'].ljust(81,'9')
    list_claims = find_transactions_by_address(address)

    if len(list_claims) == 0:
        return []

    list_claims = list_claims['hashes']

    list_output = []
    for obj in list_claims:
        list_output.append(str(obj))

    return str(list_output)
