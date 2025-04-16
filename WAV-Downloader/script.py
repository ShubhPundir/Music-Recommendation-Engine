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
        'ffmpeg_location': 'ffmpeg',  # Ensure ffmpeg is in PATH
        'quiet': False,
    }

    query = f"ytsearch1:{song_name}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(query, download=True)
        title = info_dict['entries'][0]['title'] if 'entries' in info_dict else info_dict['title']

    # Rename file
    if os.path.exists("temp.wav"):
        os.rename("temp.wav", output_filename)
        print(f"\n✅ Download complete: {output_filename} ({title})")
    else:
        print("\n❌ Download failed or file not converted.")

# Example usage
# song_query = input("Enter the name of the song: ")
song_query = "Hit the road jack"
download_name = song_query.replace(" ", "_") + ".wav"
search_and_download_wav(song_query, download_name)
