import mimetypes
from datetime import datetime
from uuid import getnode as get_mac

from myutils.utils.ip import get_ip
from .pyinfo import section_compression, section_environ, section_ldap, section_multimedia, section_os_internals, section_packages, section_py_internals, section_server_info, section_socket, section_system


def format_time(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def my_pyinfo():
    def section_custom():
        data = []

        data.append(('WAN IP Address', get_ip))

        mac = get_mac()
        data.append(('MAC Address', hex(mac)))

        return 'Custom Info', data

    data = None
    allow_import = True
    output = []
    output.append(section_custom())
    output.append(section_server_info(data))
    output.append(section_system())
    output.append(section_py_internals())
    output.append(section_os_internals())
    output.append(section_environ())
    if allow_import:
        output.append(section_compression())
    output.append(section_ldap(allow_import))
    output.append(section_socket())
    if allow_import:
        output.append(section_multimedia())
    output.append(section_packages())

    return output


def guess_type(path):
    content_type, encoding = mimetypes.guess_type(path)

    if not content_type:
        content_type = 'application/octet-stream'

        with open(path, 'rb') as fh:
            data = fh.read(4096)

        for i in range(0, 4):
            try:
                if i == 0:
                    data.decode('utf-8')
                else:
                    data[:-i].decode('utf-8')
            except UnicodeDecodeError:
                pass
            else:
                content_type = 'text/plain; charset=utf-8'
                break
    elif ';' not in content_type:
        content_type += '; charset=utf-8'

    return content_type, encoding


def is_protected_path(path):
    protected_files = (
        'etc',
        'proc',
        'log',
        'pass',
        'pwd',
        'shadow',
    )
    for part in protected_files:
        if part in path:
            return True
    return False
