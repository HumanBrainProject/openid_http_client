from requests.auth import AuthBase

class OidcAuth(AuthBase):

    def __init__(self, oidc_login_client):
        self.oidc = oidc_login_client

    def __call__(self, r):
        r.headers.update(self.oidc.get_headers())
        return r
