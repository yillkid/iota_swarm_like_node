#!/bin/bash

source tests/common.sh

POST '{"extension":"tangleid", "command":"new_claim","uuid": "V9TCFLAOGGTAQATTJBLABAG9WY", "addr":"IWHR9VJRGGTAQATTJHIJNW9OKJ","next_addr":"S9FHEJVOWHG9SHGJWNRKVNWJRX", "msg":"TestingMessage"}'
