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
