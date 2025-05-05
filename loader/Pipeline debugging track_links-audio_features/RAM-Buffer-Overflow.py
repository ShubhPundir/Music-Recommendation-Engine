import sys
import os

# Allow importing modules from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from wavScripts.audio_pipeline import download_audio_to_memory, insert_music_metadata, insert_to_db
from wavScripts.analyzer import extract_audio_features_from_buffer
from utils.logger_setup import setup_logger

logger = setup_logger()

def process_track(musicbrainz_id, track_name, artist_name):
    try:
        query = f"{track_name} {artist_name}"
        logger.info(f"[SEARCHING] YouTube search for track {musicbrainz_id}: {query}")
        audio_buf, title, channel, webpage_url = download_audio_to_memory(query)

        print(f"{title}, {channel}, {webpage_url}")
        if audio_buf is None or audio_buf.getbuffer().nbytes < 100_000:
            logger.warning(f"[SKIPPED] Invalid/too small audio for {track_name} ({musicbrainz_id})")
            return

        logger.info(f"[DOWNLOADED] {title} ({webpage_url}) for track {musicbrainz_id}")
        # insert_music_metadata(musicbrainz_id, title, channel, webpage_url)

        logger.info(f"[META INSERTED] Metadata inserted for {musicbrainz_id}: {track_name}")
        features = extract_audio_features_from_buffer(audio_buf, musicbrainz_id)
        features["track_id"] = musicbrainz_id
        insert_to_db(features)

        logger.info(f"[FEATURES INSERTED] Audio features inserted for {musicbrainz_id}: {track_name}")
    except Exception as e:
        logger.error(f"[EXCEPTION] Track {track_name} ({musicbrainz_id}) failed: {str(e)}")



def process_single_track(musicbrainz_id, track_name, artist_name):
      # Reuse existing function
    process_track(musicbrainz_id, track_name, artist_name)
if __name__ == "__main__":
    # Manually input details for the track you want to reprocess
    musicbrainz_id = "e4e291d1-5e81-4817-b787-1082b34435aa"       # Replace with actual ID
    track_name = "Simon Rattle"  # Replace with actual title
    artist_name = "Пётр Ильич Чайковский"            # Replace with actual artist

    logger.info(f"[MANUAL RUN] Processing track {musicbrainz_id}: {track_name} by {artist_name}")
    process_single_track(musicbrainz_id, track_name, artist_name)


# Track Nutcracker, Suite

# e4e291d1-5e81-4817-b787-1082b34435aa

# https://youtu.be/YSpcmqZAPGc?si=31G6XJe2Ttj5HAD9



## Main reason we couldn't insert it was due to the song's humongous length: the yt-dlp api returned a song with 1 hour 43 minutes of length
## Had to manually change it to the above record 