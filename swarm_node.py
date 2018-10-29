# -*- coding: utf-8 -*-
import subprocess
import json
import time

import iota
from iota import Iota, Address, TryteString, Transaction
from iota.crypto.signing import SignatureFragmentGenerator
from iota.crypto.kerl.conv import convertToBytes, convertToTrits, \
    trits_to_trytes, trytes_to_trits
from iota.trits import trits_from_int

from config import SEED, FULLNODE
from PoW import *

DCURL_PATH = "./deps/dcurl/build/libdcurl.so"
TXN_SECURITY_LEVEL = 2
DEPTH = 7
MWM = 9

api = Iota(FULLNODE, seed=SEED)


def insert_to_trytes(index_start, index_end, str_insert, trytes):
    trytes = trytes[:index_start] + str_insert + trytes[index_end:]

    return trytes

# Return an unused IOTA address


def generate_address():
    print("Generating an unused address ...")
    return api.get_new_addresses(count=None, index=None)

# Get transaction tips
# Parameter:
# 0: Request getTransactionToApprove RestfulAPI to fullnode
# 1: Return two null transaction
# 2: Get tips list from fullnode


def get_tips(tips_type):
    if tips_type == 0:
        return api.get_transactions_to_approve(DEPTH)
    if tips_type == 1:
        return {
            'trunkTransaction': iota.Hash(''),
            'branchTransaction': iota.Hash('')}
    if tips_type == 2:
        return api.get_tips()


def send_transfer(tag, messages, address, values, dict_tips, debug=0):
    # Initialize PoW Library
    PoWlib = PoW_load_library(DCURL_PATH)
    PoW_interface_init(PoWlib)

    # Set output transaction
    print("Start to transfer ... ")
    time_start_send = time.time()

    propose_bundle = iota.ProposedBundle()

    print("Setting output transaction ...")
    txn_output = iota.ProposedTransaction(
        address=iota.Address(address),
        value=values,
        tag=iota.Tag(tag),
        message=TryteString.from_string(messages)
    )

    propose_bundle.add_transaction(txn_output)

    # Get input address
    if int(values) > 0:
        print("DEBUG values = %s" % (str(values)))

        print("Checking input balance ...")

        dict_inputs = api.get_inputs()
        if int(dict_inputs['totalBalance']) < int(values):
            print("Balance not enough")
            return 0

    # Setting intput transaction
    if int(values) > 0:
        print("Setting input transaction ...")
        value_input = 0
        index_input = 0
        while (int(value_input) < int(values)):
            addy = iota.Address(dict_inputs['inputs'][index_input])
            addy.balance = dict_inputs['inputs'][index_input].balance
            addy.key_index = dict_inputs['inputs'][index_input].key_index
            addy.security_level = TXN_SECURITY_LEVEL

            propose_bundle.add_inputs([addy])
            value_input = value_input + int(dict_inputs['inputs'][0].balance)

        # Send unspent inputs to
        print("Setting unspent input to a new address ...")
        unspent = iota.Address(generate_address()['addresses'][0])
        propose_bundle.send_unspent_inputs_to(unspent)

    # This will get the bundle hash
    print("Bundle finalize ...")

    time_start_bundle_finz = time.time()
    propose_bundle.finalize()
    time_end_bundle_finz = time.time()
    elapsed_bundle_finz = time_end_bundle_finz - time_start_bundle_finz

    # Signing
    # If the transaction need sign, it will then sign-up the transaction
    # to fill up signature fragements
    if int(values) > 0:
        print("Signing...")
        propose_bundle.sign_inputs(iota.crypto.signing.KeyGenerator(SEED))

    trytes = propose_bundle.as_tryte_strings()

    # Get tips by getTransactionsToApprove
    trunk_hash = dict_tips['trunkTransaction']
    branch_hash = dict_tips['branchTransaction']

    # Do PoW (attach to tangle)
    elapsed_pow = 0
    time_start_pow = time.time()
    for tx_tryte in trytes:
        # Attachment timestamp insert
        timestamp = TryteString.from_trits(
            trits_from_int(int(time.time() * 1000), pad=27))
        tx_tryte = insert_to_trytes(2619, 2628, str(timestamp), tx_tryte)
        # timestamp_lower_bound = MIN_VALUE
        # timestamp_upper_bound = MAX_VALUE
        tx_tryte = insert_to_trytes(2637, 2646, str("MMMMMMMMM"), tx_tryte)

        # Tips insert - trunk
        tx_tryte = insert_to_trytes(2430, 2511, str(trunk_hash), tx_tryte)
        # Tips insert - branch
        tx_tryte = insert_to_trytes(2511, 2592, str(branch_hash), tx_tryte)

        # Do PoW for this transaction
        print("Do POW for this transaction ...")

        nonce = PoW_interface_search(PoWlib, tx_tryte, MWM)
        tx_tryte = insert_to_trytes(2646, 2673, str(nonce), tx_tryte)

        time_end_pow = time.time()
        elapsed_pow = elapsed_pow + (time_end_pow - time_start_pow)

        # Update previous tx hash for next transaction
        trunk_hash = Transaction.from_tryte_string(tx_tryte[0:2673]).hash

        print("Prepare to broadcast ...")
        try:
            api.broadcast_transactions([tx_tryte[0:2673]])
        except Exception as e:
            print("Error: %s" % (str(e.context)))

    time_end_send = time.time()
    elapsed_send = time_end_send - time_start_send

    if debug == 1:
        data = [{'platform': 'pi3', 'total_time': str(elapsed_send), 'elapsed_pow': str(
            elapsed_pow), 'elqpsed_bundle_finished': str(elapsed_bundle_finz)}]
        json_data = json.dumps(data)
        print(json_data)

#        attach_debug_message_to_tangle(json_data)
    obj_txn = api.find_transactions(bundles=[propose_bundle.hash])
    return str(obj_txn['hashes'][0])


def attach_debug_message_to_tangle(data):
    tag = "SWARMNODETESTINGDATA"
    message = TryteString.from_string(data)
    address = "BXEOYAONFPBGKEUQZDUZZZODHWJDWHEOYY9AENYF9VNLXZHXBOODCOTYXW9MGGINTEJPLK9AGOPTPODVX"
    value = 0

    # Get tips
    print("Attaching debug data to tangle ... %s" % (str(data)))
    dict_tips = get_tips(0)

    print("Debug bundle = %s" %
        (str(send_transfer(tag, message, address, value, dict_tips, 0))))


def find_transactions_by_tag(data):

    try:
        list_result = api.find_transactions(tags=[data])
    except BaseException:
        return []

    return list_result


def get_txn_msg(data):
    message = ""
    list_txn = []

    try:
        list_txn = api.get_trytes([data])
    except BaseException:
        return ""

    trytes_txn = str(list_txn['trytes'][0])
    txn = Transaction.from_tryte_string(trytes_txn)

    try:
        message = TryteString(txn.signature_message_fragment).as_string()
    except BaseException:
        return ""

    return message
