from django.shortcuts import render


def index(request):
    import os
    from .utils import markdown_from_file

    getting_started_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/getting-started.md')

    getting_started = markdown_from_file(getting_started_path)

    return render(request, 'home/index.html', {
        'getting_started': getting_started,
    })


def about(request):
    import os
    from .utils import markdown_from_file

    about_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/about.md')
    about = markdown_from_file(about_path)

    return render(request, 'home/about.html', {
        'about': about
    })


def docs(request):
    import os
    from .utils import markdown_from_file

    docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs/docs.md')

    docs = markdown_from_file(docs_path)

    return render(request, 'home/docs.html', {
        'docs': docs
    })


def license(request):
    import os

    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'LICENSE')

    if not os.path.isfile(path):
        content = ''
    else:
        with open(path, 'rb') as fh:
            data = fh.read()
        content = data.decode('utf-8')

    return render(request, 'home/plain_text.html', {
        'title': 'License',
        'heading': 'The MIT License',
        'content': content
    })
