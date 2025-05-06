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

        # logger.info(f"[DOWNLOADED] {title} ({webpage_url}) for track {musicbrainz_id}")
        # # insert_music_metadata(musicbrainz_id, title, channel, webpage_url)

        # logger.info(f"[META INSERTED] Metadata inserted for {musicbrainz_id}: {track_name}")
        # features = extract_audio_features_from_buffer(audio_buf, musicbrainz_id)
        # features["musicbrainz_id"] = musicbrainz_id
        # insert_to_db(features)

        # logger.info(f"[FEATURES INSERTED] Audio features inserted for {musicbrainz_id}: {track_name}")
    except Exception as e:
        logger.error(f"[EXCEPTION] Track {track_name} ({musicbrainz_id}) failed: {str(e)}")


if __name__ == "__main__":

    records_to_fix = [('0ec1bf3a-982d-41e3-95b5-ce09283512e5', 'motive (natalie autumn prism mix)',	'Ariana Grande'),
                    ('280f3661-cdb9-4dbe-9bd2-9a008b84f145', "If I Can't", '50 Cent'),
                    ('a466d852-3b7b-441c-ab67-d389956894e5', 'Pause 4 Porno', 'Dr. Dre')]

    for record in records_to_fix:
            
        musicbrainz_id = record[0]       # Replace with actual ID
        track_name = record[1]  # Replace with actual title
        artist_name = record[2]            # Replace with actual artist

        logger.info(f"[MANUAL RUN] Processing track {musicbrainz_id}: {track_name} by {artist_name}")
        process_track(musicbrainz_id, track_name, artist_name)


## SKIPPED SONGs

# 2025-05-04 11:27:16,132 - WARNING - [SKIPPED] Invalid/too small audio for Pause 4 Porno (a466d852-3b7b-441c-ab67-d389956894e5)

# 2025-05-04 09:53:37,246 - WARNING - [SKIPPED] Invalid/too small audio for If I Can't (280f3661-cdb9-4dbe-9bd2-9a008b84f145)

# 2025-05-04 09:34:22,636 - WARNING - [SKIPPED] Invalid/too small audio for motive (natalie autumn prism mix) (0ec1bf3a-982d-41e3-95b5-ce09283512e5)
