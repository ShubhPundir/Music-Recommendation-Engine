## LOGIC is to

# 1. Iterate in Albums' tracks object and get the artist name + track name
# 2. Fetch all 3 APIs for metadata and distribute it evenly in cockroach db's --> lyrics + mongo db's --> track_metadata
# 3. Waveform to be left after this

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

# MongoDB setup
albums_collection = db['albums']
track_metadata_collection = db['tracks_metadata']


def insert_lyrics_into_cockroach(lyrics_data):
    conn = None
    try:
        musicbrainz_id = lyrics_data.get("musicbrainz_id")
        if not musicbrainz_id:
            logger.warning("⚠️ Missing musicbrainz_id in lyrics_data. Skipping CockroachDB insertion.")
            return

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
                    musicbrainz_id,
                    lyrics_data.get("genius_lyrics"),
                    lyrics_data.get("genius_url"),
                    lyrics_data.get("lastfm_wiki_summary"),
                    lyrics_data.get("lastfm_wiki_content")
                ))
        print(f"🎶 Inserted lyrics for ID {musicbrainz_id} into CockroachDB")
        logger.info(f"🎶 Inserted lyrics for ID {musicbrainz_id} into CockroachDB")
    except Exception as e:
        print(f"⚠️ Error inserting into CockroachDB for ID {lyrics_data.get('musicbrainz_id')}: {e}")
        logger.exception(f"⚠️ Error inserting into CockroachDB for ID {lyrics_data.get('musicbrainz_id')}: {e}")
    finally:
        if conn:
            conn.close()


def process_track(artist_name, album_name, track_name):
    try:
        track_data, lyrics_data = get_track_lyrics_metadata(artist=artist_name, track=track_name)

        if not track_data or not lyrics_data:
            logger.warning(f"⚠️ Skipping '{track_name}' due to missing metadata")
            return

        if not lyrics_data.get("musicbrainz_id"):
            logger.warning(f"⚠️ Skipping '{track_name}' due to missing musicbrainz_id in lyrics_data")
            return

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

    except Exception as e:
        print(f"❌ Error processing track '{track_name}': {e}")
        logger.exception(f"❌ Error processing track '{track_name}': {e}")


def stream_albums_in_batches(batch_size=50):
    cursor = albums_collection.find({}, no_cursor_timeout=True)
    batch = []
    try:
        for album in cursor:
            batch.append(album)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
    finally:
        cursor.close()


# Main loop
for album_batch in stream_albums_in_batches():
    for album in album_batch:
        artist_name = album.get("artist") or "Unknown Artist"
        album_name = album.get("name") or "Unknown Album"
        tracks = album.get("tracks")

        if not isinstance(tracks, list) or not tracks:
            logger.warning(f"⚠️ Album '{album_name}' by '{artist_name}' has invalid or empty tracks, skipping...")
            continue

        track_names = []
        for track in tracks:
            name = track.get("name")
            if name:
                track_names.append(name)
            else:
                logger.warning(f"⚠️ Skipping unnamed track in album '{album_name}'")

        if not track_names:
            logger.warning(f"⚠️ Album '{album_name}' by '{artist_name}' has no valid track names, skipping...")
            continue

        print(f"\n🎧 Artist: {artist_name} | Album: {album_name} | Tracks: {track_names}")

        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = [executor.submit(process_track, artist_name, album_name, track_name) for track_name in track_names]
            for future in as_completed(futures):
                try:
                    future.result()  # Raises exception if any
                except Exception as e:
                    logger.exception(f"❌ Error in thread execution: {e}")

# Logging total completion
logger.info("✅ All albums processed successfully.")



# 114*11*11/3600 = 3.8316666667 hrs
# albums * avg-tracks * latency / 3600 = time in hours for loading