import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


def search_musicbrainz(artist, track):
    base_url = "https://musicbrainz.org/ws/2/recording/"
    query = f'artist:"{artist}" AND recording:"{track}"'
    params = {
        "query": query,
        "fmt": "json",
        "limit": 5
    }
    headers = {
        "User-Agent": "SongMetadataApp/1.0 (your-email@example.com)"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data.get("recordings"):
            return {"error": "No recordings found for the given song."}

        rec = data["recordings"][0]
        media = rec.get("releases", [])[0] if rec.get("releases") else {}
        release_event = media.get("release-events", [{}])[0] if media else {}

        recording_id = rec.get("id", "")
        artist_info = rec.get("artist-credit", [{}])[0].get("artist", {})
        artist_id = artist_info.get("id", "")

        return {
            "recording_id": recording_id,
            "title": rec.get("title"),
            "artist": artist_info.get("name"),
            "artist_id": artist_id,
            "album": media.get("title", ""),
            "album_id": media.get("id", ""),
            "release_date": release_event.get("date", ""),
            "country": release_event.get("area", {}).get("iso-3166-1-codes", [""])[0],
            "disambiguation": rec.get("disambiguation", ""),
            "length": rec.get("length", 0),
            "track_number": "",  # Optional: deeper logic needed
            "external_links": {
                "artist_links": get_external_links("artist", artist_id),
                "recording_links": get_external_links("recording", recording_id)
            }
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def get_external_links(entity_type, mbid):
    url = f"https://musicbrainz.org/ws/2/{entity_type}/{mbid}"
    params = {
        "fmt": "json",
        "inc": "url-rels"
    }
    headers = {
        "User-Agent": "SongMetadataApp/1.0 (your-email@example.com)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        links = {}

        for rel in data.get("relations", []):
            rel_type = rel.get("type")
            href = rel.get("url", {}).get("resource")
            if rel_type and href:
                links[rel_type] = href

        return links
    except:
        return {}


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

def search_genius(artist, track):
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    search_url = "https://api.genius.com/search"
    params = {"q": f"{artist} {track}"}

    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        hits = response.json().get("response", {}).get("hits", [])

        if not hits:
            return {}

        song_id = hits[0]["result"]["id"]
        song_url = f"https://api.genius.com/songs/{song_id}"
        song_data = requests.get(song_url, headers=headers).json()["response"]["song"]

        lyrics_url = song_data["url"]
        lyrics = scrape_lyrics(lyrics_url)

        return {
            "title": song_data["title"],
            "artist": song_data["primary_artist"]["name"],
            "lyrics": lyrics,
            "url": lyrics_url,
            "album": song_data.get("album", {}).get("name", "Unknown"),
            "release_date": song_data.get("release_date", "Unknown"),
            "song_art_image_url": song_data.get("song_art_image_url", ""),
            "annotations": [],
            "verified": song_data.get("verified", False)
        }
    except Exception as e:
        return {"error": f"Genius error: {str(e)}"}


def scrape_lyrics(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        lyrics = ""
        for div in soup.find_all("div"):
            if div.get("data-lyrics-container") == "true":
                lyrics += div.get_text(separator="\n")
        return lyrics.strip()
    except Exception as e:
        return f"Lyrics not available: {str(e)}"


def get_song_metadata(artist, track):
    return {
        "artist": artist,
        "track": track,
        "musicbrainz": search_musicbrainz(artist, track),
        "lastfm": search_lastfm(artist, track),
        "genius": search_genius(artist, track)
    }


# ----------- CLI -----------
if __name__ == "__main__":
    print("🎵 Enter the song details below to get metadata\n")
    artist = input("Enter Artist Name: ").strip()
    track = input("Enter Song Name: ").strip()

    metadata = get_song_metadata(artist, track)

    print("\n🎧 Song Metadata:\n")
    print(json.dumps(metadata, indent=4, ensure_ascii=False))

    filename = f"{artist}_{track}_metadata.json".replace(" ", "_")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Metadata saved to '{filename}'")
