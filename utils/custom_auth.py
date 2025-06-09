from dlt.sources.helpers.rest_client.auth import AuthConfigBase


class CustomAuth(AuthConfigBase):
    """Authenticator used for the Lucca API
    """

    def __init__(self, token):
        """
        Args:
            token (str): API token used for the connection'.
        """
        self.token = token

    def __call__(self, request):
        request.headers["Authorization"] = f"lucca application={self.token}"
        return request
