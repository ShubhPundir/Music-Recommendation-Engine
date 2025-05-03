import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yt_dlp
import subprocess
import io
from pprint import pprint

from database.cockroachdb import get_cockroach_connection
from wavScripts.analyzer import extract_audio_features_from_buffer

conn = get_cockroach_connection()

def download_audio_to_memory(song_query):
    try:
        # Step 1: Get bestaudio URL
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch1',
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info.get('title', 'Unknown Title')
            channel = info.get('uploader', 'Unknown Channel')
            webpage_url = info.get('webpage_url', 'Unknown URL')
            print(f"🔗 Downloading stream: {title} ({webpage_url})")

        # Step 2: Use ffmpeg to stream into memory as WAV
        ffmpeg_path = 'C:\\Users\\robot\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1.1-full_build\\bin\\ffmpeg.exe'  # Ensure ffmpeg is in PATH
        cmd = [
            ffmpeg_path, "-i", url, "-f", "wav", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1", "-"
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        audio_bytes, _ = process.communicate()

        # Returning audio data along with title, channel, and URL
        return io.BytesIO(audio_bytes), title, channel, webpage_url

    except yt_dlp.utils.DownloadError as e:
        print(f"    ❌ Download failed for song: {song_query}. Error: {str(e)}")
    except subprocess.CalledProcessError as e:
        print(f"    ❌ ffmpeg processing failed for song: {song_query}. Error: {str(e)}")
    except Exception as e:
        print(f"    ❌ An unexpected error occurred: {str(e)}")
    
    return None, None, None, None  # Return None for all in case of error

def insert_music_metadata(musicbrainz_id, track_title, channel, webpage_url, table="track_links"):
    try:
        # Construct the data dictionary to be inserted
        data = {
            "musicbrainz_id": musicbrainz_id,
            "track_title": track_title,
            "channel": channel,
            "webpage_url": webpage_url
        }

        # Insert the data into the music_metadata table
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {table} (musicbrainz_id, track_title, channel, webpage_url)
                VALUES (%(musicbrainz_id)s, %(track_title)s, %(channel)s, %(webpage_url)s)
            """, data)
            conn.commit()
            print("✅ Metadata inserted into database")
    except Exception as e:
        print(f"❌ An error occurred while inserting metadata: {str(e)}")



def insert_to_db(data, table="audio_features"):
    # Flatten the nested list fields before DB insertion
    prepared_data = {
        **data,
        **{f"mfcc_{i+1}": data.get(f"mfcc_{i+1}", 0.0) for i in range(13)},
        **{f"spectral_contrast_{i+1}": data["spectral_contrast"][i] if i < len(data["spectral_contrast"]) else 0.0 for i in range(7)},
        **{f"chroma_cens_{i+1}": data["chroma_cens_mean"][i] if i < len(data["chroma_cens_mean"]) else 0.0 for i in range(12)},
        **{f"tonnetz_{i+1}": data["tonnetz"][i] if i < len(data["tonnetz"]) else 0.0 for i in range(6)},
    }

    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO {table} (
                track_id, duration_seconds, sample_rate, tempo, loudness, danceability,
                energy, speechiness, acousticness, instrumentalness, liveness, valence,
                spectral_centroid, spectral_rolloff, spectral_bandwidth, spectral_flatness,
                zero_crossing_rate, rms_energy, tempo_variability, f0_mean, mel_mean, dynamic_range,

                mfcc_1, mfcc_2, mfcc_3, mfcc_4, mfcc_5, mfcc_6, mfcc_7,
                mfcc_8, mfcc_9, mfcc_10, mfcc_11, mfcc_12, mfcc_13,

                spectral_contrast_1, spectral_contrast_2, spectral_contrast_3, spectral_contrast_4,
                spectral_contrast_5, spectral_contrast_6, spectral_contrast_7,

                chroma_cens_1, chroma_cens_2, chroma_cens_3, chroma_cens_4,
                chroma_cens_5, chroma_cens_6, chroma_cens_7, chroma_cens_8,
                chroma_cens_9, chroma_cens_10, chroma_cens_11, chroma_cens_12,

                tonnetz_1, tonnetz_2, tonnetz_3, tonnetz_4, tonnetz_5, tonnetz_6
            ) VALUES (
                %(track_id)s, %(duration_seconds)s, %(sample_rate)s, %(tempo)s, %(loudness)s, %(danceability)s,
                %(energy)s, %(speechiness)s, %(acousticness)s, %(instrumentalness)s, %(liveness)s, %(valence)s,
                %(spectral_centroid)s, %(spectral_rolloff)s, %(spectral_bandwidth)s, %(spectral_flatness)s,
                %(zero_crossing_rate)s, %(rms_energy)s, %(tempo_variability)s, %(f0_mean)s, %(mel_mean)s, %(dynamic_range)s,

                %(mfcc_1)s, %(mfcc_2)s, %(mfcc_3)s, %(mfcc_4)s, %(mfcc_5)s, %(mfcc_6)s, %(mfcc_7)s,
                %(mfcc_8)s, %(mfcc_9)s, %(mfcc_10)s, %(mfcc_11)s, %(mfcc_12)s, %(mfcc_13)s,

                %(spectral_contrast_1)s, %(spectral_contrast_2)s, %(spectral_contrast_3)s, %(spectral_contrast_4)s,
                %(spectral_contrast_5)s, %(spectral_contrast_6)s, %(spectral_contrast_7)s,

                %(chroma_cens_1)s, %(chroma_cens_2)s, %(chroma_cens_3)s, %(chroma_cens_4)s,
                %(chroma_cens_5)s, %(chroma_cens_6)s, %(chroma_cens_7)s, %(chroma_cens_8)s,
                %(chroma_cens_9)s, %(chroma_cens_10)s, %(chroma_cens_11)s, %(chroma_cens_12)s,

                %(tonnetz_1)s, %(tonnetz_2)s, %(tonnetz_3)s, %(tonnetz_4)s, %(tonnetz_5)s, %(tonnetz_6)s
            )
        """, prepared_data)
        conn.commit()
        print("✅ Inserted into database")

# if __name__ == "__main__":
#     track_name = "Let it be"
#     artist_name = "The Beatles"
#     query = track_name + " by " + artist_name
#     audio_buf, source_track_title, channel, webpage_url = download_audio_to_memory(query)
#     ## insert source_track_title, channel, webpage_url and musicbrainz_id into a database for sanity check
#     features = extract_audio_features_from_buffer(audio_buf, 1)
#     # insert_to_db(features) ## insert into waveform table
#     pprint(features)
