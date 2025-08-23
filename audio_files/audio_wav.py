import os, sys
import re
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spectrogram_audio_files_helper.example import save_audio_file, save_spectrogram_image
from wavScripts import audio_pipeline

print("hello")
# Paths
SQL_DUMP_PATH = os.path.join("backup", "track_links", "track_links_202505061903.sql")
# TODO: Do a DB connection, SQL Dump is irreadable in machine code environments
OUTPUT_DIR = os.path.join("spectrogram", "file_jpg")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Debug: Check if SQL file exists
if not os.path.exists(SQL_DUMP_PATH):
    print(f"ERROR: SQL dump not found at {SQL_DUMP_PATH}")
    exit()

# Read SQL dump
with open(SQL_DUMP_PATH, encoding='utf-8') as f:
    content = f.read()

print("DEBUG: First 300 characters of SQL file:")
print(content[:300])
print("\n")

# Regex to extract values (tolerates spaces/newlines)
pattern = re.compile(r"\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)")
matches = pattern.findall(content)

track_list = []
for m in matches:
    musicbrainz_id, track_title, channel, url = m

    # Split artist and track
    if " - " in track_title:
        artist, track = track_title.split(" - ", 1)
    else:
        artist, track = channel, track_title

    track_list.append({
        "id": musicbrainz_id,
        "artist": artist.strip(),
        "track": track.strip()
    })

print(f"Loaded {len(track_list)} tracks from SQL dump.")

# Test limit: first 10 tracks
TEST_LIMIT = 10
tracks_to_process = track_list[:TEST_LIMIT]
print(f"Processing first {TEST_LIMIT} tracks...\n")

# Logs
log_success = open("success_log.txt", "a", encoding="utf-8")
log_fail = open("failed_log.txt", "a", encoding="utf-8")

# Process tracks
for idx, item in enumerate(tqdm(tracks_to_process, desc="Processing Tracks"), start=1):
    artist = item["artist"]
    track = item["track"]
    musicbrainz_id = item["id"]

    print(f"\n[{idx}] Processing: {track} by {artist}")

    filename_prefix = f"{musicbrainz_id}_{artist}_{track}".replace(" ", "_").replace("/", "_")
    wav_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}.wav")
    jpg_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}.jpg")

    if os.path.exists(wav_path) and os.path.exists(jpg_path):
        print(f"Skipping {track}: already processed.")
        continue

    try:
        buf, title, channel, url = audio_pipeline.download_audio_to_memory(f"{track} by {artist}")
        if not buf:
            print(f"Skipping {track}: Download failed")
            log_fail.write(f"{idx},{artist},{track},Download failed\n")
            continue

        # Save audio and spectrogram
        save_audio_file(buf, filename_prefix)
        buf.seek(0)
        save_spectrogram_image(buf, filename_prefix)

        log_success.write(f"{idx},{artist},{track},Success\n")
        print(f" Completed: {track}")

    except Exception as e:
        print(f"Error processing {track}: {e}")
        log_fail.write(f"{idx},{artist},{track},Error: {e}\n")

log_success.close()
log_fail.close()
print("\nTest run completed for 10 tracks.")
