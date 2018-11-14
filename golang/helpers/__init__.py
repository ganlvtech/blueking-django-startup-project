import os


def get_go_program_path():
    if os.name == 'nt':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'go/bin/main.exe')
    elif os.name == 'posix':
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'go/bin/main')
    else:
        path = None
    return path
