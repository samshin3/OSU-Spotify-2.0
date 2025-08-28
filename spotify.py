from requests import post, get

class SpotifySession():

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret