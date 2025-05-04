import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
## ensures that fetchDataApi is not searched within the listing of python modules, but our root directories, WOW LOL
from fetchDataApi.last_fm import search_lastfm_artist
from fetchDataApi.musicbrainz import get_artist_id_musicbrainz
from database.mongodb import db
from pprint import pprint
import csv

count: int = 0
artist_set = set()
with open('Loader/Albums  - Sheet2.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # album = row['Album']
        artist = row['Aritst/Band'].strip()  # Note the typo in column header: "Aritst/Band"

        if artist in artist_set or not artist:
            #SKIPPING for artist that we have already seen
            continue 

        artist_set.add(artist)

        lastfm_data = search_lastfm_artist(artist=artist)
        artist_id = get_artist_id_musicbrainz(artist_name=artist)

        if not lastfm_data or "error" in lastfm_data:
            print("Skipped for", f" --> {artist} NOPE :(")
            continue

        if artist_id:
            print(f"{artist} has no artist_id from musicbrainz")
            lastfm_data["musicbrainz_id"] = artist_id
        else:
            lastfm_data["musicbrainz_id"] = None

        # Insert into MongoDB
        try:
            result = db['artists'].insert_one(lastfm_data)
            print("Inserted artist with _id:", result.inserted_id, f" --> {artist} DONE :)")
        except Exception as e:
            print(f"MongoDB insert failed for {artist}: {e}")
        count += 1

print("-----"*10,":",count)
print(artist_set)