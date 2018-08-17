#!/usr/bin/env python3
from service import get_tips

TIPS_TYPE_IRI_REQULAR_ALGORITHM = 0
TIPS_TYPE_TWO_NULL_IOTA_TNX = 1

HOST = 'http://127.0.0.1'
PORT = 8000
url = str(HOST) + ":" + str(PORT)

get_tips(url, TIPS_TYPE_TWO_NULL_IOTA_TNX)
