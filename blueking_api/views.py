from django.http import JsonResponse
from django.shortcuts import render

from .blueking_api import BlueKingApi


def index(request):
    return render(request, 'blueking_api/index.html')


def get_app_access_token(request):
    bkapi = BlueKingApi()
    result = bkapi.get_app_access_token()
    return JsonResponse(result)


def get_user_access_token(request):
    bkapi = BlueKingApi()
    result = bkapi.get_user_access_token(
        openid=request.GET.get('openid'),
        openkey=request.GET.get('openkey'),
    )
    return JsonResponse(result)


def refresh_user_access_token(request):
    bkapi = BlueKingApi()
    result = bkapi.refresh_user_access_token(
        refresh_token=request.GET.get('refresh_token'),
    )
    return JsonResponse(result)


def get_user_info(request):
    bkapi = BlueKingApi()
    result = bkapi.get_user_info(
        openid=request.GET.get('openid'),
        openkey=request.GET.get('openkey'),
    )
    return JsonResponse(result)


def get_openid_openkey(request):
    bkapi = BlueKingApi()
    result = bkapi.get_openid_openkey(
        uin=request.GET.get('uin'),
        skey=request.GET.get('skey'),
    )
    return JsonResponse(result)


def verify_openid_openkey(request):
    bkapi = BlueKingApi()
    result = bkapi.verify_openid_openkey(
        openid=request.GET.get('openid'),
        openkey=request.GET.get('openkey'),
    )
    return JsonResponse(result)


def get_auth_token(request):
    bkapi = BlueKingApi()
    result = bkapi.get_auth_token(
        openid=request.GET.get('openid'),
        openkey=request.GET.get('openkey'),
    )
    return JsonResponse(result)


def send_email(request):
    bkapi = BlueKingApi()
    result = bkapi.send_email(
        title=request.GET.get('title'),
        content=request.GET.get('content'),
        access_token=request.GET.get('access_token'),
        openid=request.GET.get('openid'),
        openkey=request.GET.get('openkey'),
        receiver=request.GET.get('receiver'),
        receiver__uin=request.GET.get('receiver__uin'),
        receiver__openid=request.GET.get('receiver__openid')
    )
    return JsonResponse(result)


def send_sms(request):
    bkapi = BlueKingApi()
    result = bkapi.send_sms(
        content=request.GET.get('content'),
        access_token=request.GET.get('access_token'),
        openid=request.GET.get('openid'),
        openkey=request.GET.get('openkey'),
        receiver=request.GET.get('receiver'),
        receiver__uin=request.GET.get('receiver__uin'),
        receiver__openid=request.GET.get('receiver__openid')
    )
    return JsonResponse(result)
