import os
import requests
from dotenv import load_dotenv

load_dotenv()
LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")

def search_lastfm_track(artist, track):
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

def search_lastgm_album(artist, album):
    url = "https://ws.audioscrobbler.com/2.0/"
    headers = {
        "User-Agent": "LastFM-AlbumInfoApp/1.0"
    }
    params = {
        "method": "album.getinfo",
        "api_key": LASTFM_API_KEY,
        "artist": artist,
        "album": album,
        "format": "json"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if "album" not in data:
        raise ValueError("Album information not found.")

    album_data = data["album"]

    # Parse basic metadata
    result = {
        "name": album_data.get("name"),
        "artist": album_data.get("artist"),
        "url": album_data.get("url"),
        "playcount": album_data.get("playcount"),
        "listeners": album_data.get("listeners"),
        "tags": [tag["name"] for tag in album_data.get("tags", {}).get("tag", [])],
        "images": {img["size"]: img["#text"] for img in album_data.get("image", []) if img["#text"]},
        "tracks": [],
        "wiki_summary": album_data.get("wiki", {}).get("summary", "").split("<a")[0].strip()
    }

    # Parse track list
    for track in album_data.get("tracks", {}).get("track", []):
        result["tracks"].append({
            "name": track.get("name"),
            "duration": int(track.get("duration", 0)),
            "rank": int(track.get("@attr", {}).get("rank", 0)),
            "url": track.get("url"),
            "artist": track.get("artist", {}).get("name")
        })

    return result

# print(search_lastfm("The Beatles", "Twist and Shout"))
