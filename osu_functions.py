from ossapi import Ossapi
import tempfile

class OsuFunctions():

    def __init__(self, client_id, client_secret):
        temp_token_file = tempfile.gettempdir() + "/osu_token.pickle"
        self.api = Ossapi(client_id, client_secret, token_directory=temp_token_file)

    def get_user_id(self,username):
        user = self.api.user(user=username, key="username")
        return user.id

    def user_beatmaps(self,username, type):
        id = self.get_user_id(username)
        limit = 100 #Capped at 100 beatmaps for the sake of my computer
        beatmaps = self.api.user_beatmaps(user_id=id, type=type, limit=limit)
        return beatmaps

    def to_spotify_query(self,username, type):
        beatmaps = self.user_beatmaps(username, type)
        queries = []
        for beatmap in beatmaps:
            query = beatmap.artist+ "-" + beatmap.title
            queries.append(query)
        return queries
