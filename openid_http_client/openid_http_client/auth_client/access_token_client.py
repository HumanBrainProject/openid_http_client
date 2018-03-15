#   Copyright 2018 HumanBrainProject
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

from openid_http_client.auth_client.auth_client import AbstractAuthClient


class AccessTokenClient(AbstractAuthClient):
    """
    Access Token client

    """
    def __init__(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def refresh_token(self, old_token=None):
        return old_token
