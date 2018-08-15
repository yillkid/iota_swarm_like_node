#!/bin/bash

source tests/common.sh

POST '{"extension":"ipm", "command":"new_claim","uuid":"F9TCFLAOGGTAQATTJBLABAG9WY","channel":"HFGWKFNWGFIWGDK","next_channel":"WNFHDBRKFLHSG","msg":"TestingMessage","sign":""}'
