# coding=utf-8
from .utils import render_markdown_template, render_plain_text_file, render_special_markdown_template


def index(request):
    return render_special_markdown_template(request, 'home/index.html', 'docs/getting-started.md')


def about(request):
    return render_markdown_template(request, u'About', u'关于蓝鲸云平台', 'docs/about.md')


def docs(request):
    return render_markdown_template(request,
                                    u'Documentations',
                                    u'A Django Startup Project For Tencent Blueking',
                                    'docs/docs.md',
                                    (
                                        u'A Simplified Django Settings For Tencent Blueking',
                                    ))


def demos(request):
    return render_markdown_template(request, u'Online Demos', u'在线演示', 'docs/demos.md')


def license(request):
    return render_plain_text_file(request, u'License', u'The MIT License', 'LICENSE')
