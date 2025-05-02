## LOGIC is to

# 1. Iterate in Albums' tracks object and get the artist name + track name
# 2. Fetch all 3 APIs for metadata and distribute it evenly in cockroach db's --> lyrics + mongo db's --> track_metadata
# 3. Waveform to be left after this

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
## ensures that fetchDataApi is not searched within the listing of python modules, but our root directories, WOW LOL
from database.mongodb import db
from database.cockroachdb import get_cockroach_connection
from fetchDataApi.track_lyrics_metadata import get_track_lyrics_metadata
from pprint import pprint
from psycopg2 import sql, errors

# MongoDB setup
albums_collection = db['albums']
track_metadata_collection = db['tracks_metadata']  # new collection for metadata


# Insert into CockroachDB
def insert_lyrics_into_cockroach(lyrics_data):
    try:
        conn = get_cockroach_connection()
        with conn:
            with conn.cursor() as cursor:
                insert_query = sql.SQL("""
                    INSERT INTO lyrics (
                        musicbrainz_id,
                        genius_lyrics,
                        genius_url,
                        lastfm_wiki_summary,
                        lastfm_wiki_content
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (musicbrainz_id) DO NOTHING;
                """)
                cursor.execute(insert_query, (
                    lyrics_data.get("musicbrainz_id"),
                    lyrics_data.get("genius_lyrics"),
                    lyrics_data.get("genius_url"),
                    lyrics_data.get("lastfm_wiki_summary"),
                    lyrics_data.get("lastfm_wiki_content")
                ))
        print(f"🎶 Inserted lyrics for ID {lyrics_data.get('musicbrainz_id')} into CockroachDB")
    except Exception as e:
        print("⚠️ Error inserting into CockroachDB:", e)
    finally:
        if conn:
            conn.close()


# Main loop
for album in albums_collection.find():
    
    artist_name = album.get("artist")
    album_name = album.get("name")
    tracks = album.get("tracks", [])
    track_names = [track['name'] for track in tracks]

    print(f"Artist: {artist_name} | Album: {album_name} | Tracks: {track_names}")

    for track_name in track_names:
        track_data, lyrics_data = get_track_lyrics_metadata(artist=artist_name, track=track_name)
        
        # Insert track metadata into MongoDB
        track_metadata = {
            "artist": artist_name,
            "track": track_name,
            "album": album_name,
            "metadata": track_data
        }
        track_metadata_collection.insert_one(track_metadata)
        print(f"✅ Inserted track metadata for '{track_name}' into MongoDB")

        # Insert lyrics into CockroachDB
        insert_lyrics_into_cockroach(lyrics_data)
        print(f"Track = {track_name} inserted")

    break  # Remove this when ready to process all albums


# 114*11*11/3600 = 3.8316666667 hrs
# albums * avg-tracks * latency / 3600 = time in hours for loading

