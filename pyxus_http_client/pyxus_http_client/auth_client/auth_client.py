class AbstractAuthClient(object):
    """
    Abstract class for auth client implementation
    """
    def __init(self):
        pass

    def get_token(self):
        raise NotImplementedError

    def get_headers(self):
        raise NotImplementedError

    def refresh_token(self, token=None):
        raise NotImplementedError
