# IOTA Swarm Node

## Summary

`iota-swarm-node` is a proof-of-concept implementation of IOTA Swarm node, that
is a device with software/hardware implementing an algorithm aiming for
allowing several swarm nodes behave as a full node.

Most use cases for micropayments involve a single user or device interacting
repeatedly with a few vendors.

## Prerequisites

Install dependent packages:
```shell
$ sudo apt-get install python-pip python-setuptools python-dev python3-dev \
                       build-essential libssl-dev libffi-dev
```

Install Python package dependencies:
```shell
$ pip install -r requirements.txt
```

(Alternative) Install dependencies and activate virtualenv with Pipenv:
```shell
$ pipenv install
$ pipenv shell
```

## Build from scratch

Ensure gcc or clang available in build environment and then execute:
```shell
$ make
```

(Optional) run test suite:
```shell
$ make check
```

## Launch the service

* Launch swarm node as server:

```shell
$ python server.py
Listening on localhost:8000
```

* Generate an unused address:
```shell
$ python tests/generate_address.py
Generating an unused address ...
{u'addresses': [Address('OMAEMGRMASNBLYVFCRG9UARBBCWDIC9RGCOFTVAVJZDWISOHVMFLSW9ZL9FIJIHVVRYQLIMYBWEYP9WSX')]}
Duration: 73.5027749538 seconds
```

* Get tips from full node
```shell
$ python tests/get_tips.py
Getting tips ...
{u'duration': 484, u'branchTransaction': TransactionHash('QCPNKOXJXFERNNLTZZG9LBWDJQRLFIWDYNYQBHZJANJGXAADKNFTPWBWVDGHROVVVQWBKP9ROKRMZ9999'), u'trunkTransaction': TransactionHash('GEPJNFUNQGPDSFECJZGEWYYWYMGVWDCOELBKZQWILEUGGVHPNWFRLHNQHYKHCHPQWSQAXGYG9AIBA9999')}
Duration: 0.960033893585 seconds
```

* Send data (0 value transaction)
```shell
$ python tests/send_transfer.py
Send send transfer command ...
WIAEHXJUVO9IDZXROJEDBQLFHVFLZCIQKPLLXCGWLNZFIUJZLBZACVLZPWAKUBYLDYRZKFIDKLSAHJHEY
Duration: 1.91658091545 seconds
```

## Build the docker image

Before building the docker image, you need to build the iota-swarm-node.

```shell
  $ make
```

Build the docker image and tag with `iota-swarm-node`.

```shell
  $ docker build -t iota-swarm-node .
```

## Publish docker image to Docker Hub

1. Login to the Docker Hub.

```shell
  $ docker login
```

2. Tag docker image.

```shell
  $ docker tag iota-swarm-node DOCKER_ID_USER/iota-swarm-node
```

3. Push image to Docker Hub.

```shell
  $ docker push DOCKER_ID_USER/iota-swarm-node
```

## Licensing

`iota-swarm-node` is freely redistributable under the two-clause BSD License.
Use of this source code is governed by a BSD-style license that can be found
in the `LICENSE` file.
