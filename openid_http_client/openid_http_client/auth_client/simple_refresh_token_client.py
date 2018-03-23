#   Copyright (c) 2018, EPFL/Human Brain Project PCO
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import requests
from requests import Request

from openid_http_client.openid_http_client.auth_client.auth_client import AbstractAuthClient


def http_requests(method_name, full_url, headers=None, params=None, data=None):
    """
    Generic http request
    :param method_name:
    :param full_url:
    :param headers:
    :param params:
    :param data:
    :return:
    """
    session = requests.session()
    request = Request(method_name, full_url, headers, params=params, data=data)

    res = session.send(request.prepare())

    return res


class SimpleRefreshTokenClient(AbstractAuthClient):
    endpoints = {
        'configuration': '.well-known/openid-configuration'
    }

    scope = 'openid profile offline_access'

    def __init__(self, openid_host, client_secret, client_id, refresh_token):
        self.host = openid_host
        self.client_secret = client_secret
        self.client_id = client_id
        self.endpoints = self._fetch_endpoints()
        self.refr_token = refresh_token
        self.access_token = self.refresh_token()

    def _fetch_endpoints(self):
        """
        Fetching meaningful endpoints for Open ID calls
        :return dict: the endpoints path
        """
        res = http_requests('get', '{}/{}'.format(self.host, self.endpoints['configuration']))
        j = res.json()
        result = dict()
        result['userinfo'] = j['userinfo_endpoint']
        result['token'] = j['token_endpoint']
        return result

    def exchange_code_for_token(self, code, redirect_uri):
        """
        If no token are provided. We can request for one by providing a code and the redirect uri
        :param code:
        :param redirect_uri:
        :return:
        """
        refresh_token, access_token = self.request_refresh_token(code, redirect_uri)
        self.refr_token = refresh_token
        self.access_token = access_token

    def request_refresh_token(self, code, redirect_uri):
        """
        Http request for a new refresh token
        :param code:
        :param redirect_uri:
        :return:
        """
        params = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': redirect_uri,
            'access_type': 'offline',
            'grant_type': 'authorization_code'
        }

        res = http_requests('get', '{}/{}'.format(self.host, self.endpoints['token']), params=params)
        if res.status_code == 200:
            return res.json()['refresh_token'], res.json()['access_token']
        else:
            raise Exception('Could not get the refresh token. {}'.format(res.content))

    def get_token(self):
        if self.access_token is None:
            self.refresh_token()
        return self.access_token

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.get_token())}

    def refresh_token(self, old_refresh_token=None):
        """
        To refresh the token through the refresh token
        :return: the refreshed token
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refr_token if old_refresh_token is None else old_refresh_token,
            'grant_type': 'refresh_token'
        }
        res = http_requests('get', self.endpoints['token'], params=params)
        if res.status_code == 200:
            self.refr_token = res.json()['refresh_token']
            self.access_token = res.json()['access_token']
            return self.access_token
        else:
            raise Exception('Could not refresh the token. {}'.format(res.content))


