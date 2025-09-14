import subprocess
import io
import yt_dlp


def download_audio_from_url(url):
    """
    Downloads audio from a given URL and returns an audio buffer.
    
    Args:
        url (str): The URL of the track to download
        
    Returns:
        io.BytesIO: Audio buffer containing the downloaded audio data
        str: Title of the track
        str: Channel/uploader name
        str: Webpage URL
        
    Raises:
        Exception: If download or processing fails
    """
    try:
        # Step 1: Get bestaudio URL using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            stream_url = info['url']
            title = info.get('title', 'Unknown Title')
            channel = info.get('uploader', 'Unknown Channel')
            webpage_url = info.get('webpage_url', url)
            print(f"🔗 Downloading stream: {title} ({webpage_url})")

        # Step 2: Use ffmpeg to stream into memory as WAV
        ffmpeg_path = 'C:\\Users\\robot\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1.1-full_build\\bin\\ffmpeg.exe'
        cmd = [
            ffmpeg_path, "-i", stream_url, "-f", "wav", "-acodec", "pcm_s16le", 
            "-ar", "44100", "-ac", "1", "-"
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        audio_bytes, _ = process.communicate()

        # Return audio data along with metadata
        return io.BytesIO(audio_bytes), title, channel, webpage_url

    except yt_dlp.utils.DownloadError as e:
        print(f"    ❌ Download failed for URL: {url}. Error: {str(e)}")
        raise Exception(f"Download failed: {str(e)}")
    except subprocess.CalledProcessError as e:
        print(f"    ❌ ffmpeg processing failed for URL: {url}. Error: {str(e)}")
        raise Exception(f"Audio processing failed: {str(e)}")
    except Exception as e:
        print(f"    ❌ An unexpected error occurred: {str(e)}")
        raise Exception(f"Unexpected error: {str(e)}")
