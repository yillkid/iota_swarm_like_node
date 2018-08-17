#!/usr/bin/env python3
from service import send_transfer

TIPS_TYPE_IRI_REQULAR_ALGORITHM = 0
TIPS_TYPE_TWO_NULL_IOTA_TNX = 1

HOST = 'http://127.0.0.1'
PORT = 8000
url = str(HOST) + ":" + str(PORT)

tag = "PYTHONTEST"
message = "iHELLO"
address = "BXEOYAONFPBGKEUQZDUZZZODHWJDWHEOYY9AENYF9VNLXZHXBOODCOTYXW9MGGINTEJPLK9AGOPTPODVX"
value = 0

send_transfer(url, TIPS_TYPE_TWO_NULL_IOTA_TNX, tag, message, address, value)
