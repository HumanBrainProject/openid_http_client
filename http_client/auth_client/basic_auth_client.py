from http_client.auth_client.auth_client import AbstractAuthClient


class BasicAuthClient(AbstractAuthClient):

    def __init__(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def refresh_token(self, old_token=None):
        return old_token
