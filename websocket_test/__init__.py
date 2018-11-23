import os
import site
import sys
from io import open

dwebsocket_py2_compatible_ok = False


def fix_dwebsocket_py2_compatible(func=None):
    global dwebsocket_py2_compatible_ok
    if not dwebsocket_py2_compatible_ok:
        count = 0
        for base_dir in site.getsitepackages():
            path = os.path.join(base_dir, 'dwebsocket/backends/default/websocket.py')
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                if u'from six.moves import queue' not in data:
                    data = data.replace(u'import queue', u'from six.moves import queue')
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(data)
                    count += 1
            path = os.path.join(base_dir, 'dwebsocket/backends/default/websocket.py')
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                if u"bytes(data, 'utf-8')" in data:
                    data = data.replace(u"        if isinstance(data, str):\n            data = bytes(data, 'utf-8')", u"        if isinstance(data, six.text_type):\n            data = data.encode('utf-8')")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(data)
                    count += 1
        if count > 0 and func:
            sys.exit(1)
        dwebsocket_py2_compatible_ok = True
    return func


fix_dwebsocket_py2_compatible()
