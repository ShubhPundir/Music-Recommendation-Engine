import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wavScripts.audio_pipeline import download_audio_to_memory, insert_music_metadata, insert_to_db
from wavScripts.analyzer import extract_audio_features_from_buffer
from database.cockroachdb import get_cockroach_connection
from utils.logger_setup import setup_logger

from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2 import sql

logger = setup_logger()

BATCH_SIZE = 50  # You can tune this depending on system capacity


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


def chunks(lst, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def process_track(musicbrainz_id, track_name, artist_name):
    try:
        query = f"{track_name} {artist_name}"
        logger.info(f"[SEARCHING] YouTube search for track {musicbrainz_id}: {query}")
        audio_buf, title, channel, webpage_url = download_audio_to_memory(query)

        if audio_buf is None or audio_buf.getbuffer().nbytes < 100_000:
            logger.warning(f"[SKIPPED] Invalid/too small audio for {track_name} ({musicbrainz_id})")
            return

        logger.info(f"[DOWNLOADED] {title} ({webpage_url}) for track {musicbrainz_id}")
        insert_music_metadata(musicbrainz_id, title, channel, webpage_url)

        logger.info(f"[META INSERTED] Metadata inserted for {musicbrainz_id}: {track_name}")
        features = extract_audio_features_from_buffer(audio_buf, musicbrainz_id)
        features["track_id"] = musicbrainz_id
        insert_to_db(features)

        logger.info(f"[FEATURES INSERTED] Audio features inserted for {musicbrainz_id}: {track_name}")
    except Exception as e:
        logger.error(f"[EXCEPTION] Track {track_name} ({musicbrainz_id}) failed: {str(e)}")


def main():
    tracks = fetch_musicbrainz_ids()
    if not tracks:
        logger.warning("[NO TRACKS] Nothing to process.")
        return

    max_threads = min(8, os.cpu_count() * 2)
    logger.info(f"[STARTING] Processing {len(tracks)} tracks in batches of {BATCH_SIZE} using {max_threads} threads.")

    for batch_num, batch in enumerate(chunks(tracks, BATCH_SIZE), start=1):
        logger.info(f"[BATCH {batch_num}] Processing {len(batch)} tracks...")

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(process_track, mid, title, artist) for mid, title, artist in batch]

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.error(f"[THREAD ERROR] Uncaught exception: {e}")

    logger.info("[COMPLETE] All batches processed successfully. YOU DEATHING WORSHIPPING PIECE OF CODE, THJIS IS MY 3rd Time I am losing it")


if __name__ == "__main__":
    main()
