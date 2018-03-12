
class BasicAuthClient(object):

    def __init__(self, token):
        self.token = token

    def get_token(self):
        return self.token

    def get_headers(self):
        return {'Authorization': 'Bearer {}'.format(self.token)}

    def new_refresh_token(self, old_token=None):
        return old_token
