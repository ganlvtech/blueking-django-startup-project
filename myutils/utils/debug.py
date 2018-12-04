import re

from django.conf import settings
from django.views.debug import CallableSettingWrapper

HIDDEN_SETTINGS = re.compile('API|TOKEN|KEY|SECRET|PASS|SIGNATURE|PWD|BK_BROKER_URL|BKAPP_')

CLEANSED_SUBSTITUTE = '********************'


def cleanse_setting(key, value):
    """Cleanse an individual setting key/value of sensitive content.

    If the value is a dictionary, recursively cleanse the keys in
    that dictionary.
    """
    try:
        if HIDDEN_SETTINGS.search(key):
            cleansed = CLEANSED_SUBSTITUTE
        else:
            if isinstance(value, dict):
                cleansed = {k: cleanse_setting(k, v) for k, v in value.items()}
            else:
                cleansed = value
    except TypeError:
        # If the key isn't regex-able, just return as-is.
        cleansed = value

    if callable(cleansed):
        # For fixing #21345 and #23070
        cleansed = CallableSettingWrapper(cleansed)

    return cleansed


def get_safe_request(request):
    "Returns a dictionary of the request, with sensitive settings blurred out."
    request_dict = {}
    for k in dir(request):
        if k.isupper():
            request_dict[k] = cleanse_setting(k, getattr(request, k))
    return request_dict


def get_safe_settings():
    "Returns a dictionary of the settings module, with sensitive settings blurred out."
    settings_dict = {}
    for k in dir(settings):
        if k.isupper():
            settings_dict[k] = cleanse_setting(k, getattr(settings, k))
    return settings_dict
