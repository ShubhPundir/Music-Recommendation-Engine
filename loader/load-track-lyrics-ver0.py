## LOGIC is to

# 1. Iterate in Albums' tracks object and get the artist name + track name
# 2. Fetch all 3 APIs for metadata and distribute it evenly in cockroach db's --> lyrics + mongo db's --> track_metadata
# 3. Waveform to be left after this
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongodb import db
from database.cockroachdb import get_cockroach_connection
from fetchDataApi.track_lyrics_metadata import get_track_lyrics_metadata
from pprint import pprint
from psycopg2 import sql

# LOGGING
from utils.logger_setup import setup_logger

logger = setup_logger()

# Constants
MAX_THREADS = 3
BATCH_SIZE = 100  # Set a batch size to limit memory consumption

# MongoDB setup
albums_collection = db['albums']
track_metadata_collection = db['tracks_metadata']

def insert_lyrics_into_cockroach(lyrics_data):
    conn = None
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
        logger.info(f"🎶 Inserted lyrics for ID {lyrics_data.get('musicbrainz_id')} into CockroachDB")
    except Exception as e:
        print(f"⚠️ Error inserting into CockroachDB for ID {lyrics_data.get('musicbrainz_id')}: {e}")
        logger.exception(f"⚠️ Error inserting into CockroachDB for ID {lyrics_data.get('musicbrainz_id')}: {e}")
    finally:
        if conn:
            conn.close()

def process_track(artist_name, album_name, track_name):
    try:
        track_data, lyrics_data = get_track_lyrics_metadata(artist=artist_name, track=track_name)

        if track_data  and lyrics_data :
        
            # Insert into MongoDB
            track_metadata = {
                "artist": artist_name,
                "track": track_name,
                "album": album_name,
                "metadata": track_data
            }

            track_metadata_collection.insert_one(track_metadata)
            print(f"✅ Inserted track metadata for '{track_name}' into MongoDB")
            logger.info(f"✅ Inserted track metadata for '{track_name}' into MongoDB")

            # Insert into CockroachDB
            insert_lyrics_into_cockroach(lyrics_data)
            print(f"Track = {track_name} inserted")
            logger.info(f"Track = {track_name} inserted")

        else:
            print(f"❌ MusicBrainz ID not found for '{track_name}': {e}")
            logger.exception(f"❌ MusicBrainz ID not found for'{track_name}': {e}")


    except Exception as e:
        print(f"❌ Error processing track '{track_name}': {e}")
        logger.exception(f"❌ Error processing track '{track_name}': {e}")

def stream_albums_in_batches(batch_size=100):
    cursor = albums_collection.find()
    while True:
        batch = list(cursor.limit(batch_size))  # Fetch a batch of albums at a time
        if not batch:
            break
        yield batch

# Main loop
for album_batch in stream_albums_in_batches(batch_size=BATCH_SIZE):
    for album in album_batch:
        artist_name = album.get("artist")
        album_name = album.get("name")
        tracks = album.get("tracks", [])
        track_names = [track['name'] for track in tracks]

        print(f"\n🎧 Artist: {artist_name} | Album: {album_name} | Tracks: {track_names}")

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = [executor.submit(process_track, artist_name, album_name, track_name) for track_name in track_names]

            for future in as_completed(futures):
                try:
                    future.result()  # To raise exceptions if any
                except Exception as e:
                    logger.exception(f"❌ Error in thread execution: {e}")

logger.info("✅ All albums processed successfully.")

# 114*11*11/3600 = 3.8316666667 hrs
# albums * avg-tracks * latency / 3600 = time in hours for loading