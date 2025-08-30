from requests import post, get
import random
import string
import urllib.parse
import base64
import json

class SpotifySession():

    def __init__(self, client_id, client_secret, redirect_uri):
        self._client_id = client_id
        self._client_secret = client_secret
        self._auth_b64 = self._auth_64encode()
        self.state = self._random_string_gen(16)
        self._redirect_uri = redirect_uri

    def get_url(self):
        params = {
            "client_id": self._client_id,
            "response_type": "code",
            "redirect_uri": self._redirect_uri,
            "scope": "user-read-private user-read-email playlist-modify-public playlist-modify-private",
            "state": self.state
        }
        return f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}"
    
    def get_token(self, code=None):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + self._auth_b64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        if (code is None):
            data = {
                "grant_type": "client_credentials"
            }
        else:
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self._redirect_uri
            }

        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)

        if ("error" in json_result):
            raise SessionError(code=json_result["error"]["code"], payload=json_result["error"]["message"])
        
        self.token = SessionToken(json_result)
        self._headers = {
            "Authorization": "Bearer " + self.token.access_token,
            "Content-Type": "application/json"
        }

        self.profile = UserProfile(self._headers)
    
    def create_playlist(self, p_name="OSU! Playlist", is_public="false", collab="false", desc="My Spotify Playlist"):
        url = f"https://api.spotify.com/v1/users/{self._user_id}/playlists"
        data = {
            "name": p_name,
            "public": is_public,
            "collaborative": collab,
            "description": desc 
        }
        result = post(url,headers=self._headers, json=data)
        json_result = json.loads(result.content)

        if ("error" in json_result):
            raise SessionError(code=json_result["error"]["code"], payload=json_result["error"]["message"])
        
        return json_result
    
    def add_songs(self, playlist_id, uris):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        data = {
            "uris": uris,
        }
        result = post(url, headers=self._headers, json=data)
        json_result = json.loads(result.content)

        if ("error" in json_result):
            raise SessionError(code=json_result["error"]["code"], payload=json_result["error"]["message"])

        return json_result
    
    def search(self, query, type, limit = 1, offset = 0):
        object = type + "s"
        params = {
            "q": query,
            "type": type,
            "limit": limit,
            "offset": offset
        }
        url = f"https://api.spotify.com/v1/search?{urllib.parse.urlencode(params)}"
        result = get(url, headers=self._headers)
        json_result = json.loads(result.content)

        if ("error" in json_result):
            raise SessionError(code=json_result["error"]["code"], payload=json_result["error"]["message"])
        
        tidied_result = []

        for i in range(limit):
            item = json_result[object]["items"][i]
            details = {
                "id": item["id"],
                "name": item["name"],
                "uri": item["uri"]
            }
            tidied_result.append(details)
        
        return tidied_result
    
    # Takes one query at a time
    def get_track_uris(self, query):
        results = self.search(query, type="track")
        result = results[0]
        if result["name"] not in query:
            return ("error", query)
        return ("success", result["uri"])

    def _auth_64encode(self):
        auth = self._client_id + ":" + self._client_secret
        auth_bytes = auth.encode("utf-8")
        auth_b64 = str(base64.b64encode(auth_bytes).decode("utf-8"))
        return auth_b64

    @staticmethod
    def _random_string_gen(length):

        letters = string.ascii_letters
        random_string = "".join(random.choice(letters) for _ in range(length))
        return random_string

class SessionToken():
    
    def __init__(self,token_file):
        self.access_token = token_file["access_token"]
        self.type = token_file["token_type"]
        self.expires_int = token_file["expires_in"]

class UserProfile():

    def __init__(self, header):
        self.get_user_id(header)

    @staticmethod
    def get_user_profile(headers):
        url = "https://api.spotify.com/v1/me"
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result
    
    def get_user_id(self, headers):
        results = self.get_user_profile(headers)
        self.country = results["country"]
        self.display_name = results["display_name"]
        self.email = results["email"]
        self.explicit_content = results["explicit_content"]
        self.external_urls = results["external_urls"]
        self.followers = results["followers"]
        self.href = results["href"]
        self.id = results["id"]
        self.images = results["images"]
        self.product = results["product"]
        self.uri = results["uri"]

class SessionError(Exception):

    def __init__(self, code, payload=None):
        self.code = code
        self.message = f"Error with code {code}"
        self.message = payload
        super().__init__(self.message)
