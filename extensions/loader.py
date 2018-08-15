import importlib
import json

def load_extension(name):
    mod = importlib.import_module('extensions.' + name + ".main")
    return mod

def call_plugin(name, *args, **kwargs):
    request_command = json.dumps(args[0])
    plugin = load_extension(name)
    result = plugin.load(request_command)

    return result
