from oidc_auth_client.oidc_auth_client import HBPOidcAuthClient


def test_auth_headers():
    token = '123'
    test_uri = 'http://www.test.com/v0'
    path = '/test'

    auth_client = HBPOidcAuthClient()
    auth_client.set_client_credentials(
        'nexus-dev',
        'AOpPGrGm20-pzwHioko2EkvAhIm11YP9K-fAFnJou_Of-y-lu6T-M_UBEr04OmetcKNUcHAiVHuvCuCA_aZnqRA'
    )

    # old_token = auth_client.token
    # http_client = HttpClient('https://httpstat.us', '200', auth_client)

    # http_client.delete('')

    # assert old_token != http_client.auth_client.token

    auth_client.save_token("123")
