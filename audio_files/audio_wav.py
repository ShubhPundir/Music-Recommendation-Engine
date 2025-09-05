import os, sys
from tqdm import tqdm

# Ensure parent directory is on sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spectrogram_audio_files_helper.example import save_audio_file, save_spectrogram_image
from wavScripts import audio_pipeline
from database.cockroachdb import get_cockroach_connection


# -------------------
# Fetch tracks from DB
# -------------------
def fetch_tracks(limit=10):
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
        if " - " in track_title:
            artist, track = track_title.split(" - ", 1)
        else:
            artist, track = channel, track_title
        tracks.append({"id": musicbrainz_id, "artist": artist.strip(), "track": track.strip()})
    return tracks


# -------------------
# Process one track
# -------------------
def process_track(item, output_dir, log_success, log_fail, idx):
    artist, track, musicbrainz_id = item["artist"], item["track"], item["id"]
    print(f"\n[{idx}] Processing: {track} by {artist}")

    prefix = f"{musicbrainz_id}_{artist}_{track}".replace(" ", "_").replace("/", "_")
    wav_path, jpg_path = os.path.join(output_dir, f"{prefix}.wav"), os.path.join(output_dir, f"{prefix}.jpg")

    if os.path.exists(wav_path) and os.path.exists(jpg_path):
        print(f"Skipping {track}: already processed.")
        return

    try:
        buf, *_ = audio_pipeline.download_audio_to_memory(f"{track} by {artist}")
        if not buf:
            raise RuntimeError("Download failed")

        save_audio_file(buf, prefix)
        buf.seek(0)
        save_spectrogram_image(buf, prefix)

        log_success.write(f"{idx},{artist},{track},Success\n")
        print(f"Completed: {track}")
    except Exception as e:
        print(f"Error processing {track}: {e}")
        log_fail.write(f"{idx},{artist},{track},Error: {e}\n")


# -------------------
# Main
# -------------------
def main():
    print("Fetching tracks from database...")
    track_list = fetch_tracks(limit=10)
    print(f"Loaded {len(track_list)} tracks.\n")

    output_dir = os.path.join("spectrogram", "file_jpg")
    os.makedirs(output_dir, exist_ok=True)

    with open("success_log.txt", "a", encoding="utf-8") as log_success, \
         open("failed_log.txt", "a", encoding="utf-8") as log_fail:

        for idx, item in enumerate(tqdm(track_list, desc="Processing Tracks"), start=1):
            process_track(item, output_dir, log_success, log_fail, idx)

    print("\nTest run completed for 10 tracks.")


if __name__ == "__main__":
    main()
