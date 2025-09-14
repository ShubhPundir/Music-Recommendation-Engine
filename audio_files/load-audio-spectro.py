import os, sys
from tqdm import tqdm

# Ensure parent directory is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spectrogram_audio_files_helper.helper import save_audio_file, save_spectrogram_image
from wavScripts.download_track_via_url import download_audio_from_url
from database.cockroachdb import get_cockroach_connection
from utils.logger_setup import setup_logger


# -------------------
# Fetch tracks from DB
# -------------------
def fetch_tracks(limit=1096):
    query = """
        SELECT musicbrainz_id, track_title, channel, webpage_url
        FROM track_links
        LIMIT %s;
    """
    with get_cockroach_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()

    tracks = []
    for musicbrainz_id, track_title, channel, url in rows:
        tracks.append({
            "id": musicbrainz_id, 
            "track_title": track_title,
            "channel": channel,
            "url": url
        })
    return tracks


# -------------------
# Process one track
# -------------------
def process_track(item, output_dir, logger, idx, spectrogram_output_dir):
    musicbrainz_id, track_title, channel, url = item["id"], item["track_title"], item["channel"], item["url"]
    logger.info(f"[{idx}] Processing: {track_title} by {channel}")

    prefix = f"{musicbrainz_id}".replace(" ", "_").replace("/", "_")
    wav_path, jpg_path = os.path.join(output_dir, f"{prefix}.wav"), os.path.join(output_dir, f"{prefix}.jpg")

    if os.path.exists(wav_path) and os.path.exists(jpg_path):
        logger.info(f"Skipping id: {musicbrainz_id}::{track_title}::{url}: already processed.")
        return

    try:
        logger.debug(f"Downloading audio from URL: {url}")
        buf, title, channel_name, url = download_audio_from_url(url)
        if not buf:
            raise RuntimeError("Download failed")

        logger.debug(f"Saving audio file: {prefix}.wav")
        save_audio_file(buf, prefix, output_dir, logger)
        buf.seek(0)
        
        logger.debug(f"Generating spectrogram: {prefix}.jpg")
        save_spectrogram_image(buf, prefix, spectrogram_output_dir, logger)

        logger.info(f"Successfully processed: id:{musicbrainz_id}::{track_title}::{url}")
    except Exception as e:
        logger.error(f"Error processing id:{musicbrainz_id}::{track_title}::{url}: {e}")
        raise e


# -------------------
# Main
# -------------------
def main():
    # Setup logger for audio processing
    logger = setup_logger(
        name="AudioProcessor", 
        log_dir="logs/audio-pipeline-wav-spectrogram", 
        log_level="INFO"
    )
    
    logger.info("Starting audio processing pipeline")
    logger.info("Fetching tracks from database...")
    
    track_list = fetch_tracks(limit=1096)
    logger.info(f"Loaded {len(track_list)} tracks from database")

    output_dir = os.path.join("rec")
    os.makedirs(output_dir, exist_ok=True)
    logger.debug(f"Output directory: {output_dir}")

    spectrogram_output_dir = os.path.join("spectrogram", "file_jpg")
    os.makedirs(spectrogram_output_dir, exist_ok=True)
    logger.debug(f"Spectrogram output directory: {spectrogram_output_dir}")

    success_count = 0
    error_count = 0

    for idx, item in enumerate(tqdm(track_list, desc="Processing Tracks"), start=1):
        try:
            process_track(item, output_dir, logger, idx, spectrogram_output_dir)
            success_count += 1
        except Exception as e:
            error_count += 1
            logger.error(f"Failed to process track mb_id: {item.get('id', 'Unknown_MBID')}: {item.get('track_title', 'Unknown')} by {item.get('channel', 'Unknown')}")

    logger.info(f"Audio processing completed. Success: {success_count}, Errors: {error_count}")
    logger.info("Test run completed for 10 tracks.")


if __name__ == "__main__":
    main()
