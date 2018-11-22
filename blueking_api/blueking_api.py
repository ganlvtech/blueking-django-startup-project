# coding=utf-8
"""Tencent Blue King API

The MIT License (MIT)
Copyright (c) 2018 Ganlv

Usage

```python views.py
from django.http import JsonResponse

from .blueking_api import BlueKingApi

def send_email(request):
    bkapi = BlueKingApi()
    result = bkapi.send_email(
        title='A Test Email',
        content='Lorem ipsum',
        openid=request.session.get('openid'),
        openkey=request.session.get('openkey'),
        receiver='user@example.com'
    )
    return JsonResponse(result)
```
"""
import base64
import hashlib
import hmac
import json
import os
import random
import time
import urllib
import urlparse

import requests


class BlueKingApi:
    app_code = ''
    app_secret = ''
    env_name = ''
    permission_api_url = ''
    permission_console_url = ''
    run_mode = ''
    oauth_api_url = ''
    component_system_host = ''
    cross_domain_prefix = ''
    login_url = ''
    plain_login_url = ''

    def __init__(self, app_code=None, app_secret=None, env_name=None,
                 permission_api_url=None, permission_console_url=None, run_mode=None,
                 oauth_api_url=None, component_system_host=None,
                 cross_domain_prefix=None, login_url=None, plain_login_url=None):
        if app_code is None:
            app_code = os.environ.get('BK_APP_CODE', '')
        if app_secret is None:
            app_secret = os.environ.get('BK_SECRET_KEY', '')

        if env_name is None:
            django_conf_module = os.environ.get('DJANGO_CONF_MODULE', '')
            if 'prod' in django_conf_module:
                env_name = 'prod'
            else:
                env_name = 'test'
        elif env_name not in ('prod', 'test'):
            env_name = 'prod'

        if permission_api_url is None:
            permission_api_url = os.environ.get('BK_PERMISSION_API_URL', 'http://login.o.qcloud.com/')
        if permission_console_url is None:
            permission_console_url = os.environ.get('BK_PERMISSION_CONSOLE_URL', 'http://bk.tencent.com/campus/')
        if run_mode is None:
            django_conf_module = os.environ.get('DJANGO_CONF_MODULE', '')
            if 'prod' in django_conf_module:
                run_mode = 'PRODUCT'
            elif 'test' in django_conf_module:
                run_mode = 'TEST'
            else:
                run_mode = 'DEVELOP'

        if oauth_api_url is None:
            oauth_api_url = 'https://apigw.o.qcloud.com/'
        if component_system_host is None:
            if env_name == 'test':
                component_system_host = 'https://api-t.o.qcloud.com/c/qcloud/'
            else:
                component_system_host = 'https://api.o.qcloud.com/c/qcloud/'
        if cross_domain_prefix is None:
            cross_domain_prefix = 'https://ptlogin2.tencent.com/ho_cross_domain'
        if login_url is None:
            login_url = os.environ.get('BK_PERMISSION_API_URL', 'http://login.o.qcloud.com/')
        if plain_login_url is None:
            plain_login_url = 'http://login.o.qcloud.com/plain/'

        self.app_code = app_code
        self.app_secret = app_secret
        self.env_name = env_name

        self.permission_api_url = permission_api_url
        self.permission_console_url = permission_console_url
        self.run_mode = run_mode

        self.oauth_api_url = oauth_api_url
        self.component_system_host = component_system_host
        self.cross_domain_prefix = cross_domain_prefix
        self.login_url = login_url
        self.plain_login_url = plain_login_url

    def get_app_access_token(self):
        """获取代表应用权限的 Access Token

        注意 client_credentials 并没有访问敏感数据的权限，这个 Access Token 只是用来访问公开数据的

        TODO 这个 API 并没有被使用过
        """
        url = urlparse.urljoin(self.oauth_api_url, 'auth_api/token/')
        params = {
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'env_name': self.env_name,
            'grant_type': 'client_credentials',
        }
        response = requests.get(url, params=params, timeout=10, verify=False)
        return response.json()

    def get_user_access_token(self, openid, openkey):
        """获取用户的 Access Token"""
        url = urlparse.urljoin(self.oauth_api_url, 'auth_api/token/')
        params = {
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'env_name': self.env_name,
            'grant_type': 'authorization_code',
            'openid': openid,
            'openkey': openkey,
        }
        response = requests.get(url, params=params, timeout=10, verify=False)
        return response.json()

    def refresh_user_access_token(self, refresh_token):
        """获取用户的 Access Token"""
        url = urlparse.urljoin(self.oauth_api_url, 'auth_api/refresh_token/')
        params = {
            'app_code': self.app_code,
            'env_name': self.env_name,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
        }
        response = requests.get(url, params=params, timeout=10, verify=False)
        return response.json()

    def signature(self, msg):
        """签名算法

        :param msg: byte string
        :return: byte string
        """
        return base64.b64encode(hmac.new(self.app_secret, msg, hashlib.sha1).digest())

    def permission_api_sign_params(self, url, params, data=None):
        """权限 API 签名

        :param url: byte string
        :param params: dict
        :param data: byte string
        :return: 签名后的 params
        """
        params.update({
            'Nonce': random.randint(100000, 999999),
            'Timestamp': int(time.time()),
        })
        if not data:
            method = 'GET'
            params_to_sign = params
        else:
            method = 'POST'
            params_to_sign = params.copy()
            params_to_sign.update({
                'Data': data,
            })
        sorted_query = '&'.join(['%s=%s' % (i, params[i]) for i in sorted(params_to_sign)])
        url_components = urlparse.urlparse(url)
        raw_msg = '%s%s%s?%s' % (method, url_components.netloc, url_components.path, sorted_query)
        params.update({
            'Signature': self.signature(raw_msg),
        })
        return params

    def get_permissions(self, openid):
        """获取用户所有权限信息

        返回值参考

            {
                "code": "00",
                "permission": [
                    {
                        "function_code": "visit_index",
                        "biz_id": -1
                    }
                ],
                "permission_role": -1,
                "result": true,
                "message": "获取权限列表成功",
                "data": []
            }

        permission_role: -1 为普通用户, 2 为超级管理员
        biz_id: 业务 id，默认为 -1，似乎并没有用

        :param openid:
        :return
        :rtype dict
        """
        url = urlparse.urljoin(self.permission_api_url, 'permission/get_permissions/')
        params = {
            'app_code': self.app_code,
            'uin': openid,
        }
        params = self.permission_api_sign_params(url, params)
        response = requests.get(url, params=params, timeout=10, verify=False)
        return response.json()

    def check_failed_url(self, info='', is_ajax=False):
        """权限不足提示页面的 URL

        :param info: byte string 提示信息
        :param is_ajax: True|False 是否是 ajax 请求
        :return 权限不足提示页面的 URL
        """
        params = urllib.urlencode({
            'app_code': self.app_code,
            'run_mode': self.run_mode,
            'info': info,
        })
        if is_ajax:
            url = self.permission_console_url + 'permission_center/check_failed_ajax/?' + params
        else:
            url = self.permission_console_url + 'permission_center/check_failed/?' + params
        return url

    def component_api_sign_params(self, url, params, data=None):
        """组件 API 签名

        TODO 暂时未使用

        :param url: byte string
        :param params: dict
        :param data: byte string
        :return: 签名后的 params
        """
        params.update({
            'bk_timestamp': int(time.time()),
            'bk_nonce': random.randint(1, 2147483647),
        })
        if not data:
            method = 'GET'
            params_to_sign = params
        else:
            method = 'POST'
            params_to_sign = params.copy()
            params_to_sign.update({
                'data': data,
            })
        sorted_query = '&'.join(['%s=%s' % (i, params[i]) for i in sorted(params_to_sign)])
        url_components = urlparse.urlparse(url)
        raw_msg = '%s%s?%s' % (method, url_components.path, sorted_query)
        params.update({
            'signature': self.signature(raw_msg),
        })
        return params

    def develop_login_url(self, redirect_url, is_plain=False):
        """本地测试时若使用蓝鲸登录，跳转的 URL

        :param redirect_url: 返回页面的连接
        :param is_plain: True|False 是否使用内嵌式小窗登录
        :return 登录的 URL
        """
        c_url = self.cross_domain_prefix + '?' + urllib.urlencode({
            'tourl': redirect_url,
        })
        params = urllib.urlencode({
            'app_code': self.app_code,
            'c_url': c_url,
        })
        if is_plain:
            url = self.plain_login_url + '?' + params
        else:
            url = self.login_url + '?' + params
        return url

    def get_user_info(self, openid, openkey):
        """获取用户基本信息"""
        url = urlparse.urljoin(self.component_system_host, 'compapi/oidb/get_user_info/')
        params = {
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'openid': openid,
            'openkey': openkey,
        }
        response = requests.get(url, params=params, timeout=10, verify=False)
        return response.json()

    @staticmethod
    def transform_uin(uin):
        """转换 uin 格式

        :param uin: cookie 中的 uin
        :return 正常格式的 QQ 号，不带 o0 前缀
        :rtype str
        """
        if uin[0] == 'o':
            return str(int(uin[1:]))
        else:
            return uin

    def get_openid_openkey(self, uin, skey):
        """通过 uin 和 skey 获取 openid 和 openkey

        :param uin: 正常格式的 QQ 号，不带 o0 前缀（如果有的话也会自动去掉）
        :param skey: cookie 中的 skey
        """
        uin = self.transform_uin(uin)
        url = urlparse.urljoin(self.component_system_host, 'compapi/oidb/get_openid_openkey/')
        params = {
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'uin': uin,
            'skey': skey,
        }
        response = requests.get(url, params=params, timeout=10, verify=False)
        return response.json()

    def verify_openid_openkey(self, openid, openkey):
        """验证 openid 和 openkey"""
        url = urlparse.urljoin(self.component_system_host, 'compapi/oidb/verify_openid_openkey/')
        params = {
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'openid': openid,
            'openkey': openkey,
        }
        response = requests.get(url, params=params, timeout=10, verify=False)
        return response.json()

    def get_auth_token(self, openid, openkey):
        """获取 Auth Token

        Auth Token 似乎和 Access Token 是相同的

        TODO 这个 API 并没有被使用过
        """
        url = urlparse.urljoin(self.component_system_host, 'compapi/auth/get_auth_token/')
        data = {
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'openid': openid,
            'openkey': openkey,
        }
        data = json.dumps(data)
        response = requests.post(url, data=data, timeout=10, verify=False)
        return response.json()

    def send_email(self, title, content, access_token=None, openid=None, openkey=None, receiver=None, receiver__uin=None, receiver__openid=None):
        """发送邮件

        因为由用户 `openid`, `openkey` 和本应用的 `app_code`, `app_secret` 可以获取到 `access_token`，
        所以可以只提供 `openid` 和 `openkey`，也可以只提供 `access_token`。

        参考 https://bk.tencent.com/campus/developer-center/comp_perm/doc/api/send_mail_for_external_user/

        :param title: 邮件标题
        :param content: 邮件内容
        :param access_token: 任意一个用户的 access_token（通常为当前用户的）
        :param openid: 任意一个用户的 openid（通常为当前用户的）
        :param openkey: 对应的 openkey
        :param receiver: 接受者邮箱地址，以逗号分隔
        :param receiver__uin: 接受者 QQ 号，以逗号分隔
        :param receiver__openid: 接受者 openid，以逗号分隔
        :return: 返回的 json
        :rtype: dict
        """
        url = urlparse.urljoin(self.component_system_host, 'compapi/qcloud_cmsi/send_mail_for_external_user/')
        data = {
            'access_token': access_token,
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'openid': openid,
            'openkey': openkey,
            'receiver': receiver,
            'receiver__uin': receiver__uin,
            'receiver__openid': receiver__openid,
            'title': title,
            'content': content,
        }
        data = json.dumps(data)
        response = requests.post(url, data=data, timeout=10, verify=False)
        return response.json()

    def send_sms(self, content, access_token=None, openid=None, openkey=None, receiver=None, receiver__uin=None, receiver__openid=None):
        """发送短信

        因为由用户 `openid`, `openkey` 和本应用的 `app_code`, `app_secret` 可以获取到 `access_token`，
        所以可以只提供 `openid` 和 `openkey`，也可以只提供 `access_token`。

        参考 https://bk.tencent.com/campus/developer-center/comp_perm/doc/api/send_sms_for_external_user/

        :param content: 短信内容
        :param access_token: 任意一个用户的 access_token（通常为当前用户的）
        :param openid: 任意一个用户的 openid（通常为当前用户的）
        :param openkey: 对应的 openkey
        :param receiver: 接受者电话号码，以逗号分隔
        :param receiver__uin: 接受者 QQ 号，以逗号分隔
        :param receiver__openid: 接受者 openid，以逗号分隔
        :return: 返回的 json
        :rtype: dict
        """
        url = urlparse.urljoin(self.component_system_host, 'compapi/qcloud_cmsi/send_sms_for_external_user/')
        data = {
            'access_token': access_token,
            'app_code': self.app_code,
            'app_secret': self.app_secret,
            'openid': openid,
            'openkey': openkey,
            'receiver': receiver,
            'receiver__uin': receiver__uin,
            'receiver__openid': receiver__openid,
            'content': content,
        }
        data = json.dumps(data)
        response = requests.post(url, data=data, timeout=10, verify=False)
        return response.json()
