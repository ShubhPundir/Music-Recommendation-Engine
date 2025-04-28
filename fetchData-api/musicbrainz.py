import os
import requests
from dotenv import load_dotenv

load_dotenv()
MUSICBRAINZ_USER_AGENT = os.getenv("MUSICBRAINZ_USER_AGENT")

base_url = "https://musicbrainz.org/ws/2"
# Custom headers to avoid throttling (use a unique User-Agent)
headers = {
    "User-Agent": MUSICBRAINZ_USER_AGENT
}

def search_musicbrainz(artist, track):
    query = f'artist:"{artist}" AND recording:"{track}"'
    params = {
        "query": query,
        "fmt": "json",
        "limit": 5
    }

    try:
        response = requests.get(f"{base_url}/recording", params=params, headers=headers)
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
            "length": rec.get("length", 0)
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def get_artist_id_musicbrainz(artist_name):
    artist_query = f"{base_url}/artist/"
    params = {
        "query": f"artist:{artist_name}",
        "fmt": "json"
    }

    artist_response = requests.get(artist_query, params=params, headers=headers)
    artist_data = artist_response.json()
    
    # Check for multiple artist matches and find the best match
    artists = artist_data.get("artists", [])
    if not artists:
        return None
    
    # Optionally, print all artist names to check what's returned
    print(f"Found artists: {[artist['name'] for artist in artists]}")
    
    # Assume the first match is the correct one or try to find exact match
    for artist in artists:
        if artist_name.lower() == artist['name'].lower():
            print(artist["id"])
            return artist["id"]

    # If no exact match, return the first artist
    return artists[0]["id"]

def get_album_tracks_musicbrainz(artist_name, album_name):

    # 1. Search for artist and get ID
    artist_id = get_artist_id_musicbrainz(artist_name)

    if not artist_id:
        print(f"Artist '{artist_name}' not found.")
        return []

    # 2. Search for release-group (album)
    release_group_query = f"{base_url}/release-group/?artist={artist_id}&releasegroup={album_name}&type=album&fmt=json"
    release_group_response = requests.get(release_group_query, headers=headers)
    release_group_data = release_group_response.json()

    release_group = release_group_data.get("release-groups", [])
    if not release_group:
        print(f"Album '{album_name}' not found for artist '{artist_name}'.")
        return []

    release_group_id = release_group[0]["id"]

    # 3. Search for releases (specific versions of the album)
    releases_query = f"{base_url}/release?release-group={release_group_id}&fmt=json"
    releases_response = requests.get(releases_query, headers=headers)
    releases_data = releases_response.json()

    release = releases_data.get("releases", [])
    if not release:
        print(f"No releases found for album '{album_name}'.")
        return []

    release_id = release[0]["id"]

    # 4. Get tracks (recordings) from the release
    tracks_query = f"{base_url}/release/{release_id}?inc=recordings&fmt=json"
    tracks_response = requests.get(tracks_query, headers=headers)
    tracks_data = tracks_response.json()

    track_titles = []
    for media in tracks_data.get("media", []):
        for track in media.get("tracks", []):
            track_titles.append(track["title"])

    return track_titles
