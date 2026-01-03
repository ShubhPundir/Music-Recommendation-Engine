import subprocess
import io
import yt_dlp
import time


def _download_and_stream_audio(url, ydl_opts, ffmpeg_path):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        stream_url = info['url']
        title = info.get('title', 'Unknown Title')
        uploader = info.get('uploader', 'Unknown Channel')
        webpage_url = info.get('webpage_url', url)
        print(f"🔗 Downloading stream: {title} by {uploader} ({webpage_url})")

    cmd = [
        ffmpeg_path, "-i", stream_url, "-f", "wav", "-acodec", "pcm_s16le",
        "-ar", "44100", "-ac", "1", "-"
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    audio_bytes, _ = process.communicate()

    return io.BytesIO(audio_bytes), title, uploader, webpage_url

def download_audio_from_url(url, track_title=None, channel=None, retries=3, delay=5):
    """
    Downloads audio from a given URL and returns an audio buffer. If the direct download fails,
    it retries with a search query constructed from track_title and channel.
    """
    ffmpeg_path = 'C:\\Users\\RAH\\Downloads\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe'
    initial_url = url

    for attempt in range(retries):
        current_url = url if attempt == 0 else f"ytsearch1:{track_title} {channel}" # Use search query for retries
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'extract_flat': False,
            'default_search': 'ytsearch1' if attempt > 0 else None # Only set default search for retries
        }

        try:
            return _download_and_stream_audio(current_url, ydl_opts, ffmpeg_path)
        except yt_dlp.utils.DownloadError as e:
            print(f"    ❌ Download failed for URL: {current_url}. Error: {str(e)}")
            if attempt < retries - 1 and track_title and channel:
                print(f"    🔄 Retrying with search query: {track_title} by {channel} (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
                continue
            else:
                raise Exception(f"Download failed after {retries} attempts for {initial_url}: {str(e)}")
        except subprocess.CalledProcessError as e:
            print(f"    ❌ ffmpeg processing failed for URL: {current_url}. Error: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                raise Exception(f"Audio processing failed after {retries} attempts for {initial_url}: {str(e)}")
        except Exception as e:
            print(f"    ❌ An unexpected error occurred for URL: {current_url}: {str(e)}")
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                raise Exception(f"Unexpected error after {retries} attempts for {initial_url}: {str(e)}")
    return None, None, None, None # Should not be reached but for safety
