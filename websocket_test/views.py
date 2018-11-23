from django.shortcuts import render
from dwebsocket import accept_websocket

from . import fix_dwebsocket_py2_compatible


@accept_websocket
@fix_dwebsocket_py2_compatible
def index(request):
    if not request.is_websocket():
        return render(request, 'websocket_test/index.html')
    else:
        request.websocket.send(b'WebSocket Test')
        for message in request.websocket:
            request.websocket.send(b'Reply: ' + message)
