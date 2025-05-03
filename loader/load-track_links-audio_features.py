import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wavScripts.audio_pipeline import download_audio_to_memory, insert_music_metadata, insert_to_db
from wavScripts.analyzer import extract_audio_features_from_buffer
from database.cockroachdb import get_cockroach_connection
from utils.logger_setup import setup_logger  # Make sure this is the correct path

from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2 import sql


logger = setup_logger()


def fetch_musicbrainz_ids():
    try:
        with get_cockroach_connection() as conn:
            with conn.cursor() as cursor:
                query = sql.SQL("SELECT musicbrainz_id, title, artist FROM track_reference WHERE musicbrainz_id IS NOT NULL")
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info(f"Fetched {len(results)} tracks from database.")
                return results
    except Exception as e:
        logger.error(f"Database fetch error: {e}")
        return []


def process_track(musicbrainz_id, track_name, artist_name):
    try:
        query = f"{track_name} {artist_name}"
        logger.info(f"[SEARCHING] Searching YouTube for track {musicbrainz_id}: {query}")
        audio_buf, title, channel, webpage_url = download_audio_to_memory(query)

        if audio_buf is None:
            logger.warning(f"[ERROR] Skipping {track_name} ({musicbrainz_id}) — download failed.")
            return

        logger.info(f"[DOWNLOADED] Downloaded: {title} ({webpage_url}) for track {musicbrainz_id}")

        insert_music_metadata(musicbrainz_id, title, channel, webpage_url)
        logger.info(f"[CORRECT] Metadata inserted for track {musicbrainz_id}: {track_name}")

        features = extract_audio_features_from_buffer(audio_buf, musicbrainz_id)
        features["track_id"] = musicbrainz_id
        insert_to_db(features)
        logger.info(f"[AUDIO FEATURES] Audio features inserted for track {musicbrainz_id}: {track_name}")

    except Exception as e:
        logger.error(f"[EXCEPTION] Error processing track {track_name} ({musicbrainz_id}): {str(e)}")


def main():
    tracks = fetch_musicbrainz_ids()

    if not tracks:
        logger.warning("[NO TRACKS] No tracks to process.")
        return

    max_threads = min(8, os.cpu_count() * 2)

    logger.info(f"[STARTING] Starting processing with {max_threads} threads.")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(process_track, mid, title, artist) for mid, title, artist in tracks]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"[ERROR] Uncaught exception in thread: {e}")

    logger.info(f"[DONE] All tracks processed, I  hope this death worshipping piece of code works")

if __name__ == "__main__":
    main()
