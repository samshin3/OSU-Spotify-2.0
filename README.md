# OSU to Spotify 2.0

# Introduction

This is a new flask app that is made based off the original [OSU-to-Spotify-Playlist-Converter](https://github.com/samshin3/OSU-to-Spotify-Playlist-Converter) repo.

The app calls the OSU! API to get a user's beatmaps on their profile, and converts the songs and compiles them into a Spotify playlist.

This version of the website is more complete and has more abilities and is more optimized for webpage use.

# Key changes

1. App takes user input from html page instead of terminal
2. Used concurrent features to speed up API calls
3. Improved Spotify and OSU API classes creating cleaner code

# How to use the app

There are a few things that need to be done prior to running this app:
1. Create an app on Spotify for developers:
    - Follow the [Getting Started](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) guide
    - Take note of the client id and client secret

2. Create an OAuth application on OSU!
    - Follow the [Quickstart](https://tybug.dev/ossapi/creating-a-client.html)
    - take note of the client id and client secret

After getting these values, clone the repo, create a virtual environment and install the requirements:

Mac
```
git clone https://github.com/samshin3/OSU-to-Spotify-Playlist-Converter
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Windows
```
git clone https://github.com/samshin3/OSU-to-Spotify-Playlist-Converter
python -m venv env
.\Scripts\activate.bat
pip install -r requirements.txt
```

Create a new .env file and copy past in the code below, fill in the values accordingly:

```
SPOTIFY_CLIENT_ID = "Your Spotify Client ID"
SPOTIFY_CLIENT_SECRET = "Your Spotify Client Secret"
OSU_CLIENT_ID = "Your OSU Client ID"
OSU_CLIENT_SECRET = "Your OSU Client Secret"
```

Save it and run the main.py file!