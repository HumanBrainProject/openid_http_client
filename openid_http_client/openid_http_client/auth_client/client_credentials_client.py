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

from openid_http_client.auth_client.auth_client import AbstractAuthClient


class ClientCredentialsClient(AbstractAuthClient):
    endpoints = {
        'configuration': '.well-known/openid-configuration'
    }

    scope = 'openid profile offline_access'

    def __init__(self, openid_host, client_secret, client_id):
        self.host = openid_host
        self.client_secret = client_secret
        self.client_id = client_id
        self.endpoints = self._fetch_endpoints()
        self.token = None

    def get_token(self):
        if self.token is None:
            return self.refresh_token()
        return self.token

    def _fetch_endpoints(self):
        """
        Fetching meaningful endpoints for Open ID calls
        :return dict: the endpoints path
        """
        res = self.__http_requests('get',
                                   '{}/{}'.format(self.host, self.endpoints['configuration']))
        j = res.json()
        result = dict()
        result['userinfo'] = j['userinfo_endpoint']
        result['token'] = j['token_endpoint']
        return result

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.get_token())}

    def refresh_token(self, old_token=None):
        """
        To refresh the token
        :return: the refreshed token
        """
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        res = self.__http_requests('post', '{}/{}'.format(self.host, self.endpoints['token']), data=data)
        if res.status_code == 200:
            token = res.json()['access_token']
            self.token = token
            return token
        else:
            raise Exception('Could not get the token. {}'.format(res.content))

    def __http_requests(self, method_name, full_url, headers=None, params=None, data=None):
        session = requests.session()
        request = Request(method_name, full_url, headers, params=params, data=data)
        res = session.send(request.prepare())
        return res
