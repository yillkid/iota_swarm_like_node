# How to write extensions for IOTA Swarm node

This is a guide for how to write a swarm node extension.

## Create a python module in extensions directory
```shell
$ mkdir extensions/example
$ touch extensions/example/__init__.py
```

## Extension file naming rules
* Extension name is directory name
* New a extension entry file: main.py

```shell
$ touch extensions/example/main.py
```

## Entry point
```shell
$ vi extensions/example/main.py
```
```
def load(data):
    print("Hello it's a sample extension!")
```
