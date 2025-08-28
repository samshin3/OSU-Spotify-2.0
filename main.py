import os
from dotenv import load_dotenv
from flask import Flask, redirect, request, session
import secrets



load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
app_secret_key = secrets.token_hex(32)

app = Flask(__name__)
app.secret_key = app_secret_key

@app.route("/")
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

@app.route("/login")
def login():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"

if __name__ == "__main__":
    
    app.run(host = "0.0.0.0", port=5000, debug=True)