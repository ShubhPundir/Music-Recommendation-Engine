import yt_dlp
import os

def search_and_download_wav(song_name, output_filename="output.wav"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': 'temp.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }
        ],
        'ffmpeg_location': 'C:\\Users\\robot\\AppData\\Local\\Microsoft\\WinGet\\Packages\\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\\ffmpeg-7.1.1-full_build\\bin',  # Ensure ffmpeg is in PATH
        'quiet': False,
        'default_search': 'ytsearch1',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(song_name, download=True)

            # Handle search result entry
            if 'entries' in info_dict:
                info_dict = info_dict['entries'][0]

            # Extract metadata
            title = info_dict.get('title', 'Unknown Title')
            duration = info_dict.get('duration', 'Unknown Duration')
            channel = info_dict.get('uploader', 'Unknown Channel')
            url = info_dict.get('webpage_url', 'Unknown URL')

        # Rename downloaded file
        temp_file = "temp.wav"
        if os.path.exists(temp_file):
            os.rename(temp_file, output_filename)
            print(f"\n✅ Download complete: {output_filename}")
            print(f"🎵 Title      : {title}")
            print(f"⏱  Duration   : {duration} seconds")
            print(f"📺 Channel    : {channel}")
            print(f"🔗 URL        : {url}\n")
        else:
            print("\n❌ Download failed or file not converted.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

# Example usage
song_query = "Please Please Me"
artist_name = "The Beatles"
download_name = f"{song_query.replace(' ', '_')}-{artist_name.replace(' ', '_')}.wav"
search_and_download_wav(f"{song_query} by {artist_name}", download_name)
