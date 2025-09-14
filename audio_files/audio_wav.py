import os, sys
from tqdm import tqdm

# Ensure parent directory is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spectrogram_audio_files_helper.example import save_audio_file, save_spectrogram_image
from wavScripts import audio_pipeline
from database.cockroachdb import get_cockroach_connection
from utils.logger_setup import setup_logger


# -------------------
# Fetch tracks from DB
# -------------------
def fetch_tracks(limit=2):
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
        tracks.append({"id": musicbrainz_id, "url": url})
    return tracks


# -------------------
# Process one track
# -------------------
def process_track(item, output_dir, logger, idx, spectrogram_output_dir):
    artist, track, musicbrainz_id = item["artist"], item["track"], item["id"]
    logger.info(f"[{idx}] Processing: {track} by {artist}")

    prefix = f"{musicbrainz_id}_{artist}_{track}".replace(" ", "_").replace("/", "_")
    wav_path, jpg_path = os.path.join(output_dir, f"{prefix}.wav"), os.path.join(output_dir, f"{prefix}.jpg")

    if os.path.exists(wav_path) and os.path.exists(jpg_path):
        logger.info(f"Skipping {track}: already processed.")
        return

    try:
        logger.debug(f"Downloading audio for: {track} by {artist}")
        buf, *_ = audio_pipeline.download_audio_to_memory(f"{track} by {artist}")
        if not buf:
            raise RuntimeError("Download failed")

        logger.debug(f"Saving audio file: {prefix}.wav")
        save_audio_file(buf, prefix, output_dir)
        buf.seek(0)
        
        logger.debug(f"Generating spectrogram: {prefix}.jpg")
        save_spectrogram_image(buf, prefix, spectrogram_output_dir)

        logger.info(f"Successfully processed: {track} by {artist}")
    except Exception as e:
        logger.error(f"Error processing {track} by {artist}: {e}")
        raise e ## fix this as well?


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
            logger.error(f"Failed to process track {idx}: {item.get('track', 'Unknown')} by {item.get('artist', 'Unknown')}")

    logger.info(f"Audio processing completed. Success: {success_count}, Errors: {error_count}")
    logger.info("Test run completed for 10 tracks.")


if __name__ == "__main__":
    main()
