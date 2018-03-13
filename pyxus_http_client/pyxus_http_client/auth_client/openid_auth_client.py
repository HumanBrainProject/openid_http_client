import os
import requests
from requests import Request

from pyxus_http_client.auth_client.auth_client import AbstractAuthClient


class OpenIDAuthClient(AbstractAuthClient):
    endpoints = {
        'configuration': '.well-known/openid-configuration'
    }

    scope = 'openid profile offline_access'

    def __init__(self, openid_host, client_secret=None, client_id=None, refresh_token=None,
                 refresh_token_file_path='refresh_token'):
        self.host = openid_host
        self.client_secret = client_secret
        self.client_id = client_id
        self.refresh_token_file_path = refresh_token_file_path
        if refresh_token is not None and self.validate_token(refresh_token):
            self.save_token(refresh_token)
            self.token = refresh_token
        else:
            self.token = self._get_refresh_token_from_file()

        self.endpoints = self._fetch_endpoints()

    def set_client_credentials(self, client_id, client_secret):
        self.client_secret = client_secret
        self.client_id = client_id

    def _fetch_endpoints(self):
        res = self.__http_requests('get',
                                   '{}/{}'.format(self.host, self.endpoints['configuration']))
        j = res.json()
        result = dict()
        result['userinfo'] = j['userinfo_endpoint']
        result['token'] = j['token_endpoint']
        return result

    def _get_refresh_token_from_file(self):
        try:
            with open(self.refresh_token_file_path) as refresh_token_file:
                return refresh_token_file.readline()
        except Exception as e:
            print e
            return None

    def save_token(self, token):
        try:
            with open(self.refresh_token_file_path, 'wt') as refresh_token_file:
                os.chmod(self.refresh_token_file_path, 0o600)
                refresh_token_file.write(token)
        except Exception as e:
            print e
            return None

    def exchange_code_for_token(self, code, redirect_uri):
        token = self.request_refresh_token(code, redirect_uri)
        self.save_token(token)
        self.refresh_token = token

    def request_refresh_token(self, code, redirect_uri):
        params = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': redirect_uri,
            'access_type': 'offline',
            'grant_type': 'authorization_code'
        }

        res = self.__http_requests('get', '{}/{}'.format(self.host, self.endpoints['token']),
                                   params=params)
        if res.status_code == 200:
            return res.json()['refresh_token']
        else:
            raise Exception('Could not get the refresh token. {}'.format(res.content))

    def get_token(self):
        if self.token is None:
            raise Exception(
                'No refresh token. Please use the exchange_code_for_token method beforehand')
        return self.token

    def get_headers(self):
        if self.token is None:
            raise Exception(
                'No refresh token. Please use the exchange_code_for_token method beforehand')
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def validate_token(self, token):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        res = self.__http_requests('get', '{}/{}'.format(self.host, self.endpoints['userinfo']),
                                   headers=headers)
        return res.status_code < 300

    def refresh_token(self, old_token=None):
        """
        To refresh the token
        :param old_token: previous token
        :return: the refreshed token
        """
        if self.client_id is None and self.client_secret is None:
            raise Exception('Error Client ID and Client Secret not set properly. '
                            'Maybe you should try with using the set_client_credentials method, '
                            'before calling this method.')
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.get_token() if old_token is None else old_token,
            'grant_type': 'refresh_token'
        }
        res = self.__http_requests('get', '{}/{}'.format(self.host, self.endpoints['token']),
                                   params=params)
        if res.status_code == 200:
            token = res.json()['refresh_token']
            self.save_token(token)
            self.token = token
            return token
        else:
            raise Exception('Could not refresh the token. {}'.format(res.content))

    def __http_requests(self, method_name, full_url, headers=None, params=None, data=None):
        session = requests.session()
        request = Request(method_name, full_url, headers, params=params, data=data)

        res = session.send(request.prepare())

        return res
