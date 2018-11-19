# coding=utf-8
import json
import os
import urlparse

import requests


class BlueKingApi:
    app_code = ''
    app_secret = ''
    env_name = ''
    oauth_api_url = ''
    component_system_host = ''

    def __init__(self, app_code=None, app_secret=None, env_name=None, oauth_api_url=None, component_system_host=None):
        if app_code is None:
            app_code = os.environ.get('BK_APP_CODE', '')
        if app_secret is None:
            app_secret = os.environ.get('BK_SECRET_KEY', '')
        if env_name is None:
            # if 'prod' in (os.environ.get('DJANGO_CONF_MODULE', '').lower()):
            #     env_name = 'prod'
            # else:
            #     env_name = 'test'
            env_name = 'prod'
        elif env_name not in ('prod', 'test'):
            env_name = 'prod'
        if oauth_api_url is None:
            oauth_api_url = 'https://apigw.o.qcloud.com/'
        if component_system_host is None:
            # if env_name == 'test':
            #     component_system_host = 'https://api-t.o.qcloud.com/c/qcloud/'
            # else:
            #     component_system_host = 'https://api.o.qcloud.com/c/qcloud/'
            component_system_host = 'https://api.o.qcloud.com/c/qcloud/'
        self.app_code = app_code
        self.app_secret = app_secret
        self.env_name = env_name
        self.oauth_api_url = oauth_api_url
        self.component_system_host = component_system_host

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

    def get_openid_openkey(self, uin, skey):
        """通过 uin 和 skey 获取 openid 和 openkey"""
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
        params = {}
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
        response = requests.post(url, params=params, data=data, timeout=10, verify=False)
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
        params = {}
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
        response = requests.post(url, params=params, data=data, timeout=10, verify=False)
        return response.json()
