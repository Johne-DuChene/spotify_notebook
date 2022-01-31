'''This project is for getting familiar with spotipy. The data gathered from here will be used for
EDA in the notebook in the same directory as this file.'''

'''Following the example in the docs, we'll pull the names of all the albums created by the
artist Birdy.'''

# spotipy, meant to make integrating requests to the spotify API easier.
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# to get environment variables.
import os
from dotenv import load_dotenv
# We'll be using the defaultdict datatype from the collections
# module as it never raises a key error.
from collections import defaultdict
import pandas as pd

# read our .env file (if present)
load_dotenv()

# I pull my credentials from my environment.
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENTSECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# this is essentially our cursor object. We specify the auth manager and pass in our
# credentials, which should be saved as environment variables.
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = SPOTIPY_CLIENT_ID,
    client_secret = SPOTIPY_CLIENT_SECRET, redirect_uri = SPOTIPY_REDIRECT_URI,
    scope = "user-read-recently-played"))

# this function is to be used in case a song is absent from the df.
def find_song(name, year):
    '''Returns a dataframe for a song given its name and year.'''
    song_data = defaultdict()
    # here we execute a query with the SpotiPy search function. The q parameter accepts a string
    # and can be one of the following values: album, artist, track, year, upc,
    # tag:hipster, tag:new, isrc, and genre.
    results = sp.search(q = 'track: {} year: {}'.format(name, year), limit = 1)
    # if null, return nothing.
    if results['tracks']["items"] == []:
        return None
    # results is a dictionary which can be indexed
    results = results['tracks']["items"][0]
    # id is pulled
    id = results["id"]
    # now we use the id to query the api for audio features
    audio_features = sp.audio_features(id)[0]
    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]
    for key, value in audio_features.items():
        song_data[key] = value
    
    return pd.DataFrame(song_data).to_csv("song_data.csv")


results = sp.current_user_recently_played()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])