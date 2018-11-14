_ip = None


def get_ip():
    global _ip
    if _ip is None:
        import requests
        _ip = requests.get('http://ip-api.com/json').json()['query']
    return _ip
