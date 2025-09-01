from ossapi import Ossapi
import tempfile
import os

class OsuFunctions():

    def __init__(self, client_id, client_secret):
        token_dir = os.path.join(tempfile.gettempdir(), "osu_tokens")
        os.makedirs(token_dir, exist_ok=True)
        self.api = Ossapi(client_id, client_secret, token_directory=token_dir)

    def get_user_id(self,username):
        try:
            user = self.api.user(user=username, key="username")
            self.user_id = user.id
        except ValueError:
            raise ValueError("User Not Found")

    def get_beatmaps(self, type):
        limit = 100 #Capped at 100 beatmaps for the sake of my computer
        beatmaps = self.api.user_beatmaps(user_id=self.user_id, type=type, limit=limit)

        if (not beatmaps):
            raise ValueError("Playlist is empty")
        
        return beatmaps

    @staticmethod
    def to_spotify_query(beatmaps):
        queries = []
        for beatmap in beatmaps:
            query = beatmap.artist+ "-" + beatmap.title
            queries.append(query)
        return queries

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    OSU_client_id = os.getenv("OSU_CLIENT_ID")
    OSU_client_secret = os.getenv("OSU_CLIENT_SECRET")
    osu_session = OsuFunctions(OSU_client_id, OSU_client_secret)