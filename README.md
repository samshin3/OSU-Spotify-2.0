# OSU to Spotify 2.0

A live version of this website is currently running on Vercel:
[OSU! to Spotify 2.0](https://osu-spotify-2-0.vercel.app)

# Introduction

This is a new flask app that is made based off the original [OSU-to-Spotify-Playlist-Converter](https://github.com/samshin3/OSU-to-Spotify-Playlist-Converter) repo.

The app calls the OSU! API to get a user's beatmaps on their profile, and converts the songs and compiles them into a Spotify playlist.

This version of the website is more complete and has more abilities and is more optimized for webpage use.

# Key changes

1. App takes user input from html page instead of terminal
2. Used concurrent features to speed up API calls
3. Improved Spotify and OSU API classes creating cleaner code
