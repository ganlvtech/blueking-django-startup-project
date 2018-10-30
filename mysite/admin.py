import string
import random
from django.http import HttpResponse
from django.utils.html import escape

def random_password():
    chars = string.letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for i in range(random.randint(12, 16)))


def init(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    if User.objects.filter(username='admin').count() > 0:
        return HttpResponse('admin has already exists.')

    password = random_password()
    User.objects.create_superuser('admin', 'admin@example.com', password)

    html = """
    Superuser created.<br>
    Username <input type="text" readonly value="admin">.<br>
    Password <input type="text" readonly value=\"%s\">.<br>
    This operation can't be done twice.
    """ % (escape(password))
    return HttpResponse(html)
