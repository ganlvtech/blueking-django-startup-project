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
    host = request.POST.get('host', settings.EMAIL_HOST)
    port = int(request.POST.get('port', settings.EMAIL_PORT))
    username = request.POST.get('username', settings.EMAIL_HOST_USER)
    password = request.POST.get('password', settings.EMAIL_HOST_PASSWORD)
    email = request.POST.get('email')
    if not username or not password:
        return render(request, 'send_email/index.html', {
            'error': u'未设置 SMTP 账号，发送邮件失败'
        })

    try:
        from django.core.mail.backends.smtp import EmailBackend
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
