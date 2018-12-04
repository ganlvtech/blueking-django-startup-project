import requests

_ip = None


def get_ip():
    global _ip
    if _ip is None:
        _ip = requests.get('http://ip-api.com/json').json()['query']
    return _ip
