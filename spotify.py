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
        self.state = self.random_string_gen(16)
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
    
    def get_token(self, code):
        url = "https://accounts.spotify.com/api/token"
        auth = self._client_id + ":" + self._client_secret
        auth_bytes = auth.encode("utf-8")
        auth_b64 = str(base64.b64encode(auth_bytes).decode("utf-8"))
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self._redirect_uri
        }
        header = {
            "Authorization": "Basic " + auth_b64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        result = post(url, headers=header, data=data)
        json_result = json.loads(result.content)

        if "error" in json_result:
            raise PermissionError
        
        self._token = json_result["access_token"]
        self._headers = {
            "Authorization": "Bearer " + self._token,
            "Content-Type": "application/json"
        }
    
    def get_user_profile(self):
        url = "https://api.spotify.com/v1/me"
        result = get(url, headers=self._headers)
        json_result = json.loads(result.content)
        return json_result
    
    def get_user_id(self):
        results = self.get_user_profile()
        self._user_id = results["id"]
    
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
        return json_result
    
    def add_songs(self, playlist_id, uris):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        data = {
            "uris": uris,
        }
        result = post(url, headers=self._headers, json=data)
        json_result = json.loads(result.content)
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
    
    def get_track_uris(self, query):
        results = self.search(query, type="track")
        result = results[0]
        if result["name"] not in query:
            return ("error", query)
        return ("success", result["uri"])

    @staticmethod
    def random_string_gen(length):

        letters = string.ascii_letters
        random_string = "".join(random.choice(letters) for _ in range(length))
        return random_string
    
    @staticmethod
    def client_cred(client_id, client_secret):
        url = "https://accounts.spotify.com/api/token"
        auth = client_id + ":" + client_secret
        auth_bytes = auth.encode("utf-8")
        auth_b64 = str(base64.b64encode(auth_bytes).decode("utf-8"))

        body = {
            "grant_type": "client_credentials",
        }
        headers = {
            "Authorization": "Basic " + auth_b64,
            "Content-Type": "application/x-www-form-urlencoded" 
        }
        result = post(url=url, headers=headers, data=body)
        json_result = json.loads(result.content)
        return json_result