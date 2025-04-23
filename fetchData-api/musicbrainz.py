import requests
from dotenv import load_dotenv

load_dotenv()
MUSICBRAINZ_USER_AGENT = os.getenv("MUSICBRAINZ_USER_AGENT")

def search_musicbrainz(artist, track):
    base_url = "https://musicbrainz.org/ws/2/recording/"
    query = f'artist:"{artist}" AND recording:"{track}"'
    params = {
        "query": query,
        "fmt": "json",
        "limit": 5
    }
    headers = {
        "User-Agent": MUSICBRAINZ_USER_AGENT
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
