# coding=utf-8
from django.shortcuts import render


def index(request):
    import re
    from django.core.mail import send_mail
    from django.template.loader import get_template

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

    from django.conf import settings
    if not settings.EMAIL_HOST_PASSWORD:
        return render(request, 'send_email/index.html', {
            'error': u'未设置 SMTP 账号，禁止发送邮件'
        })

    send_mail(
        subject,
        content,
        'ganlv@outlook.com',
        ['ganlvtech@qq.com'],
        html_message=html_content
    )

    return render(request, 'send_email/index.html', {
        'ok': True
    })
