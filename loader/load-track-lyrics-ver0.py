## LOGIC is to

# 1. Iterate in Albums' tracks object and get the artist name + track name
# 2. Fetch all 3 APIs for metadata and distribute it evenly in cockroach db's --> lyrics + mongo db's --> track_metadata
# 3. Waveform to be left after this

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
## ensures that fetchDataApi is not searched within the listing of python modules, but our root directories, WOW LOL
from database.mongodb import db
from fetchDataApi.track_lyrics_metadata import get_track_lyrics_metadata
from pprint import pprint

collection = db['albums']

for albums in collection.find():
    # pprint()
    artist_name = albums.get("artist")
    tracks = albums.get("tracks")
    track_names = [track['name'] for track in tracks]
    print(f"Artist: {artist_name} --> {track_names}")
    for track in track_names:
        track_data, lyrics_data = get_track_lyrics_metadata(artist=artist_name, track=track)
        pprint(track_data)
        print("---"*10)
        pprint(lyrics_data)
    break

# 117*11*112/3600 = 40 hrs

