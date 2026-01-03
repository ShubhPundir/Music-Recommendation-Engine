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

def search_lastfm_album(artist, album):
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

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if "album" not in data:
            raise ValueError("Album information not found.")

        album_data = data["album"]

        ## In some cases, album_data["tags"] is not a dictionary (as expected), but a string — which causes .get("tag") to fail.
        tags_data = album_data.get("tags")
        if isinstance(tags_data, dict):
            tags = [tag["name"] for tag in tags_data.get("tag", [])]
        else:
            tags = []

        image_data = album_data.get("image")
        if isinstance(image_data, list):
            images = {img["size"]: img["#text"] for img in image_data if img.get("#text")}
        else:
            images = {}

        # Parse basic metadata
        result = {
            "name": album_data.get("name"),
            "artist": album_data.get("artist"),
            "url": album_data.get("url"),
            "playcount": album_data.get("playcount"),
            "listeners": album_data.get("listeners"),
            "tags": tags,
            "images": images, ##{img["size"]: img["#text"] for img in album_data.get("image") or [] if img["#text"]},
            "tracks": [],
            "wiki_summary": album_data.get("wiki", {}).get("summary", "").split("<a")[0].strip()
        }

        # Parse track list
        for track in album_data.get("tracks", {}).get("track", []):
            result["tracks"].append({
                "name": track.get("name"),
                "duration": int(track.get("duration") or 0), ## Incase None --> 0
                "rank": int(track.get("@attr", {}).get("rank") or 0),
                "url": track.get("url"),
                "artist": track.get("artist", {}).get("name")
            })

        return result
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print ({"error": f"Album '{album}' by '{artist}' not found in the Last.fm database."})
            return
        else:
            print ({"error": f"HTTP error occurred: {http_err}"})
            return
    except Exception as e:
        print({"error": f"An error occurred: {str(e)}"})
        return 

def search_lastfm_artist(artist):
    if not LASTFM_API_KEY:
        return {"error": "Last.fm API key is missing. Please set LASTFM_API_KEY in your .env file."}

    base_url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getinfo",
        "artist": artist,
        "api_key": LASTFM_API_KEY,
        "format": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        artist_data = response.json().get("artist", {})

        # Genres / Tags
        tags = [tag["name"] for tag in artist_data.get("tags", {}).get("tag", [])]

        # Similar artists
        similar_artists = []
        for similar in artist_data.get("similar", {}).get("artist", []):
            similar_artists.append({
                "name": similar.get("name"),
                "url": similar.get("url")
            })

        # Wiki summary and content
        wiki = artist_data.get("bio", {})
        summary = wiki.get("summary", "").split("<a")[0].strip()
        content = wiki.get("content", "").strip()

        return {
            "name": artist_data.get("name"),
            "tags": tags,
            "similar_artists": similar_artists,
            "wiki": {
                "published": wiki.get("published", ""),
                "summary": summary,
                "content": content
            }
        }

    except requests.exceptions.HTTPError as http_err:
        print( {"error": f"HTTP error occurred: {http_err}"} )
        return None
    except Exception as e:
        print({"error": f"An error occurred: {str(e)}"})
        return None


# print(search_lastfm("The Beatles", "Twist and Shout"))
