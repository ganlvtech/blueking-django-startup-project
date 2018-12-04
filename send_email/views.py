# coding=utf-8
import re

from django.core.mail import send_mail
from django.core.mail.backends.smtp import EmailBackend
from django.shortcuts import render
from django.template.loader import get_template


def index(request):
    html_template = get_template('send_email/email.html')
    subject = 'Hello from django.qcloudapps.com'
    content = 'A Django Startup Project For Tencent Blueking.\n' \
              'A Simplified Django Settings For Tencent Blueking.\n' \
              'Home Page https://django.qcloudapps.com/'

    html_content = html_template.render({
        'title': subject,
        'lines': content.split('\n'),
    })
    html_content = re.sub(r'\s+', ' ', html_content)

    if request.method == 'GET':
        return render(request, 'send_email/index.html', {
            'email': html_content
        })

    host = request.POST.get('host')
    port = int(request.POST.get('port'))
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    if not username or not password:
        return render(request, 'send_email/index.html', {
            'error': u'未设置 SMTP 账号，发送邮件失败'
        })

    try:
        connection = EmailBackend(
            host=host,
            port=port,
            username=username,
            password=password
        )
        send_mail(
            subject,
            content,
            username,
            [email],
            html_message=html_content,
            connection=connection
        )
    except Exception as e:
        return render(request, 'send_email/index.html', {
            'error': e.message
        })

    return render(request, 'send_email/index.html', {
        'ok': True
    })
