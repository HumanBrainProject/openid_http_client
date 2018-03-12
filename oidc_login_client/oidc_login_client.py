import requests

from oidc_login_client.oidc_auth import OidcAuth


class HBPOidcLogin(object):
    refresh_token_file_path = 'refresh_token'
    user_info_endpoint = 'userinfo'
    host = 'https://services.humanbrainproject.eu/oidc'
    authorize_endpoint = 'authorize'
    token_endpoint = 'token'
    internal_auth_endpoint = 'http://localhost:5000/auth'

    def __init__(self, client_id, client_secret, redirect_uri,
                 scope='openid profile offline_access'):
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret
        self.client_id = client_id
        self.refresh_token = self._get_refresh_token_from_file()

    def _get_refresh_token_from_file(self):
        try:
            with open(self.refresh_token_file_path) as refresh_token_file:
                return refresh_token_file.readline()
        except Exception as e:
            return None

    def exchange_code_for_token(self, code):
        token = self.request_refresh_token(code)
        self.save_token(token)
        self.refresh_token = token

    def request_refresh_token(self, code):
        params = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'access_type': 'offline',
            'grant_type': 'authorization_code'
        }

        res = requests.get('{}/{}'.format(self.host, self.token_endpoint), params=params)

        return res.json()['refresh_token']

    def save_token(self, token):
        try:
            with open(self.refresh_token_file_path, 'w') as refresh_token_file:
                refresh_token_file.write(token)
        except Exception as e:
            return None

    def get_token(self):
        if self.refresh_token is None:
            raise Exception(
                'No refresh token. Please use the exchange_code_for_token method beforehand')
        return self.refresh_token

    def get_headers(self):
        if self.refresh_token is None:
            raise Exception(
                'No refresh token. Please use the exchange_code_for_token method beforehand')
        return {'Authorization': 'Bearer {}'.format(self.refresh_token)}

    def validate_token(self, token):
        headers = {'Authorization': 'Bearer {}'.format(token)}
        res = requests.get('{}/{}'.format(self.host, self.user_info_endpoint), headers=headers)
        return res.status_code < 300

    def new_refresh_token(self, old_token=None):
        """
        To refresh the token
        :param old_token: previous token
        :return: the refreshed token
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.get_token() if old_token is None else old_token,
            'grant_type': 'refresh_token'
        }
        res = requests.get('{}/{}'.format(self.host, self.token_endpoint), params=params)
        token = res.json()['refresh_token']
        self.save_token(token)
        self.refresh_token = token
        return token


oidc = HBPOidcLogin('nexus-dev',
                        'AOpPGrGm20-pzwHioko2EkvAhIm11YP9K-fAFnJou_Of-y-lu6T-M_UBEr04OmetcKNUcHAiVHuvCuCA_aZnqRA',
                        'http://localhost')


# oidc.exchange_code_for_token('mElaNo')

# def get_function(headers, params):
#     req = requests.session()
#     req.auth = OidcAuth(oidc)
#     res = req.get('https://google.com', headers=headers)
#     print res

#
# oidc.authentication_request()
