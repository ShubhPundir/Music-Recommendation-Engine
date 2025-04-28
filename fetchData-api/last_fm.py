import os
import requests
from dotenv import load_dotenv

load_dotenv()
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")


def search_lastfm(artist, track):
    if not LASTFM_API_KEY:
        return {"error": "Last.fm API key is missing. Please set LASTFM_API_KEY in your .env file."}

    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getInfo",
        "artist": artist,
        "track": track,
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        track_info = response.json().get("track", {})

        tags = [tag["name"] for tag in track_info.get("toptags", {}).get("tag", [])]
        wiki = track_info.get("wiki", {})
        summary = wiki.get("summary", "")
        content = wiki.get("content", "")

        return {
            "tags": tags,
            "wiki": {
                "published": wiki.get("published", ""),
                "summary": summary,
                "content": content
            },
            "similar_tracks": []  # Optional: add support later
        }
    except Exception as e:
        return {"error": f"Last.fm error: {str(e)}"}

# print(search_lastfm("The Beatles", "Twist and Shout"))