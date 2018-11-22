import os

from django.conf import settings
from django.shortcuts import render


def read_file(path):
    from io import open
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def markdown_from_file(path):
    import markdown
    html = markdown.markdown(read_file(path), extensions=['fenced_code', 'tables'])
    return html


def render_special_markdown_template(request, template_name, relative_path):
    """
    :param request:
    :param template_name:
    :param relative_path: markdown relative path from BASE_DIR like 'docs/demos.md'
    :return:
    """
    path = os.path.join(settings.BASE_DIR, relative_path)
    content = markdown_from_file(path)
    return render(request, template_name, {
        'content': content
    })


def render_markdown_template(request, title, heading, relative_path, leads=None):
    """
    :param request:
    :param title:
    :param heading:
    :param leads:
    :param relative_path: markdown relative path from BASE_DIR like 'docs/demos.md'
    :return:
    """
    if leads is None:
        leads = ()
    path = os.path.join(settings.BASE_DIR, relative_path)
    content = markdown_from_file(path)
    return render(request, 'home/markdown.html', {
        'title': title,
        'heading': heading,
        'leads': leads,
        'content': content,
    })

def render_plain_text_content(request, title, heading, content):
    return render(request, 'home/plain_text.html', {
        'title': title,
        'heading': heading,
        'content': content,
    })


def render_plain_text_file(request, title, heading, relative_path):
    """
    :param request:
    :param title:
    :param heading:
    :param relative_path: file relative path from BASE_DIR like 'LICENSE'
    :return:
    """
    path = os.path.join(settings.BASE_DIR, relative_path)
    content = read_file(path)
    return render_plain_text_content(request, title, heading, content)
