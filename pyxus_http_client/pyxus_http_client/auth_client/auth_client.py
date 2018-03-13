class AbstractAuthClient(object):

    def __init(self):
        pass

    def get_token(self):
        raise NotImplementedError

    def get_headers(self):
        raise NotImplementedError

    def refresh_token(self, token=None):
        raise NotImplementedError
