import os
import re
import sys
from tqdm import tqdm

# Ensure parent directory is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'audio_files')))

from load_audio_spectro import process_track
from utils.logger_setup import setup_logger

def parse_failed_tracks(log_path):
    failed = []
    # Pattern: Failed to process track N: <track> by <artist>
    pattern = re.compile(r"Failed to process track \d+: (.+) by (.+)")
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.search(line)
            if m:
                track, artist = m.group(1).strip(), m.group(2).strip()
                failed.append({"artist": artist, "track": track})
    return failed

def main():
    log_path = os.path.join("logs", "audio-pipeline-wav-spectrogram", "errors.log")
    failed_tracks = parse_failed_tracks(log_path)
    print(f"Found {len(failed_tracks)} failed tracks in log.")

    output_dir = os.path.join("rec")
    spectrogram_output_dir = os.path.join("spectrogram", "file_jpg")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(spectrogram_output_dir, exist_ok=True)

    logger = setup_logger(
        name="AudioProcessorRerun",
        log_dir="logs/audio-pipeline-wav-spectrogram",
        log_level="INFO"
    )

    for idx, item in enumerate(tqdm(failed_tracks, desc="Reprocessing Failed Tracks"), start=1):
        # We don't have musicbrainz_id here, so set to 'unknown' or try to fetch if needed
        item_full = {"id": "unknown", "artist": item["artist"], "track": item["track"]}
        try:
            process_track(item_full, output_dir, logger, idx, spectrogram_output_dir)
        except Exception as e:
            logger.error(f"Still failed to process: {item['track']} by {item['artist']}")

if __name__ == "__main__":
    main()