import requests
import json

g_id = 0
config_cache = None
session = requests.Session()

def init(port):
    """Handshake with the coordinator, return config"""
    global g_id
    g_id += 1
    req = {
        'jsonrpc': '2.0',
        'method': 'getconfig',
        'params': {},
        'id': g_id,
    }
    url = "http://localhost:%d/" % (port,)
    response = session.post(url, data=json.dumps(req))
    rsp = response.json()
    config = rsp['result']['config']
    return config

def clear_init_cache():
    """Clear config cache at end of episode"""
    global config_cache
    config_cache = None

def cached_init(port):
    """Handshake with the coordinator, return config"""
    global config_cache
    print("cached init with existing", config_cache)
    if not config_cache:
        config_cache = init(port)
    return config_cache

def step(port, state):
    """Send state to the coordinator, return actions"""
    global g_id
    g_id += 1
    req = {
        'jsonrpc': '2.0',
        'method': 'step',
        'params': { 'state': state, },
        'id': g_id,
    }
    url = "http://localhost:%d/" % (port,)
    response = session.post(url, data=json.dumps(req))
    rsp = response.json()
    action = rsp['result']['action']
    return action
