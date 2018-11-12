import mimetypes


def format_time(timestamp):
    from datetime import datetime
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def my_pyinfo():
    from .pyinfo import section_server_info, section_system, section_py_internals, section_os_internals, section_environ, section_compression, section_ldap, section_socket, section_multimedia, section_packages

    data = None
    allow_import = True
    output = []
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


def markdown_from_file(path):
    import markdown
    from io import open

    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()

    html = markdown.markdown(data, extensions=['fenced_code', 'tables'])

    return html


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

    return content_type, encoding
