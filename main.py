import os
from dotenv import load_dotenv
from flask import Flask, redirect, request, render_template, flash
import secrets
from spotify import SpotifySession, SessionError
from osu_functions import OsuFunctions
from concurrent.futures import ThreadPoolExecutor
import sys

load_dotenv()

if (len(sys.argv) > 1):
    Spotify_client_id = os.getenv("TEST_CLIENT_ID")
    Spotify_client_secret = os.getenv("TEST_CLIENT_SECRET")
    redirect_uri = "http://localhost:5500/callback"
else:
    Spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    Spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = "https://osu-spotify-2-0.vercel.app/callback"

api_session = SpotifySession(Spotify_client_id, Spotify_client_secret, redirect_uri)

OSU_client_id = os.getenv("OSU_CLIENT_ID")
OSU_client_secret = os.getenv("OSU_CLIENT_SECRET")
osu_session = OsuFunctions(OSU_client_id, OSU_client_secret)

app_secret_key = secrets.token_hex(32)
app = Flask(__name__)
app.secret_key = app_secret_key


@app.route("/")
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route("/login")
def login():
    return redirect(api_session.get_url())

@app.route("/callback")
def callback():
    if "error" in request.args:
        return redirect("/error")
    
    if request.args["state"] != api_session.state:
        return redirect("/error")
    
    try:
        api_session.get_token(request.args["code"])

    except:
        return redirect("/error")
    
    return redirect("/make-playlist")

@app.route("/error")
def error():
    return "there was an error"

@app.route("/make-playlist")
def make_playlist():
    return render_template("make_playlist.html")

@app.route("/submit", methods=["POST"])
def submit():
    p_name = request.form.get("p_name")
    username = request.form.get("Username")
    beatmap_type = request.form.get("Beatmap_type")
    is_public = request.form.get("is_public")
    collab = request.form.get("collab")
    desc = request.form.get("desc")

    try:
        osu_session.get_user_id(username=username)
    except ValueError:
        flash("OSU! Player Not Found")
        return redirect("/make-playlist")
    
    try:
        beatmaps = osu_session.get_beatmaps(type=beatmap_type)
    except ValueError:
        flash("Beatmaps is empty!")
        return redirect("/make-playlist")
    
    try:
        playlist = api_session.create_playlist(p_name=p_name, is_public=is_public, collab=collab, desc=desc)
    except SessionError:
        flash("Could not make playlist")
        return redirect("/make-playlist")

    try:
        queries = osu_session.to_spotify_query(beatmaps=beatmaps)

        with ThreadPoolExecutor() as executor:
            uri_list = list(executor.map(api_session.get_track_uris, queries))

        errors = list(map(lambda x: x[1], filter(lambda x: "error" in x, uri_list)))
        uri_list = list(map(lambda x: x[1], filter(lambda x: "error" not in x, uri_list)))
        api_session.add_songs(playlist_id=playlist["id"], uris=uri_list)

        return f"Successfully added {len(uri_list)} songs. \n could not find the following tracks: \n{errors}\n"
    except:
        flash("User Not Found")
        return redirect("/make-playlist")

if (len(sys.argv) > 1):
    app.run(host="0.0.0.0", port=5500, debug=True)