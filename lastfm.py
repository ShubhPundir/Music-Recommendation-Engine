#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

API_KEY = "da87e77d2348b4b9227b38b60d31f7e9"  # Replace this with your real key
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
HEADERS = {"User-Agent": "LastFMExplorer/1.0"}

def get_track_info(artist, track):
    params = {
        "method": "track.getInfo",
        "api_key": API_KEY,
        "artist": artist,
        "track": track,
        "format": "json"
    }

    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    data = response.json()

    if 'track' not in data:
        print("No track info found.")
        return

    track_info = data['track']
    print(f"\n🎵 Track: {track_info.get('name')}")
    print(f"🎤 Artist: {track_info.get('artist', {}).get('name')}")
    print(f"▶️ Play Count: {track_info.get('playcount')}")
    print(f"❤️ Listeners: {track_info.get('listeners')}")
    print(f"🌐 URL: {track_info.get('url')}")

    print("\n🏷️ Top Tags:")
    for tag in track_info.get('toptags', {}).get('tag', []):
        print(f" - {tag['name']}")

get_track_info("BTS", "Dynamite")


# In[2]:


import requests
import time

LASTFM_API_KEY = "da87e77d2348b4b9227b38b60d31f7e9"  # 🔁 Replace with your key

HEADERS = {"User-Agent": "MetadataFusion/1.0"}
MB_BASE = "https://musicbrainz.org/ws/2"
LF_BASE = "http://ws.audioscrobbler.com/2.0/"

# Step 1: Get Artist ID from MusicBrainz
def search_artist_mb(artist_name):
    url = f"{MB_BASE}/artist"
    params = {"query": artist_name, "fmt": "json"}
    response = requests.get(url, params=params, headers=HEADERS)
    data = response.json()
    return data['artists'][0] if data['artists'] else None

# Step 2: Get releases/albums from MusicBrainz
def get_releases_mb(artist_id):
    url = f"{MB_BASE}/release"
    params = {"artist": artist_id, "fmt": "json", "limit": 5}
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json().get('releases', [])

# Step 3: Get recordings (tracks) for a release
def get_recordings_mb(release_id):
    url = f"{MB_BASE}/recording"
    params = {"release": release_id, "fmt": "json", "limit": 5}
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json().get('recordings', [])

# Step 4: Get Last.fm track info
def get_lastfm_track_info(artist, track):
    params = {
        "method": "track.getInfo",
        "api_key": LASTFM_API_KEY,
        "artist": artist,
        "track": track,
        "format": "json"
    }
    response = requests.get(LF_BASE, params=params, headers=HEADERS)
    data = response.json()
    return data.get("track")

# Main combined function
def explore_artist_data(artist_name):
    print(f"🔍 Searching for artist: {artist_name}")
    artist = search_artist_mb(artist_name)
    if not artist:
        print("Artist not found.")
        return

    print(f"\n🎤 Artist: {artist['name']}")
    print(f"📇 MBID: {artist['id']}")
    print(f"🌍 Country: {artist.get('country')}")
    print(f"🎭 Type: {artist.get('type')}")

    releases = get_releases_mb(artist['id'])
    if not releases:
        print("No releases found.")
        return

    print("\n💿 Albums:")
    for rel in releases:
        print(f" - {rel['title']} ({rel.get('date', 'unknown')})")

    selected_release = releases[0]
    print(f"\n📀 Getting tracks from: {selected_release['title']}")

    tracks = get_recordings_mb(selected_release['id'])
    if not tracks:
        print("No tracks found.")
        return

    print("\n🎶 Track Info (with Last.fm user data):")
    for track in tracks:
        time.sleep(1)  # ⏱️ To avoid hitting rate limits
        lf_info = get_lastfm_track_info(artist['name'], track['title'])
        if not lf_info:
            print(f" - {track['title']}: ❌ Not found on Last.fm")
            continue

        print(f"\n🎵 {track['title']}")
        print(f"▶️ Play Count: {lf_info.get('playcount')}")
        print(f"👥 Listeners: {lf_info.get('listeners')}")
        tags = [tag['name'] for tag in lf_info.get('toptags', {}).get('tag', [])]
        print(f"🏷️ Tags: {', '.join(tags) if tags else 'None'}")
        print(f"🔗 {lf_info.get('url')}")

# 👇 Example usage:
explore_artist_data("BTS")


# In[3]:


import requests
import json

API_KEY = "da87e77d2348b4b9227b38b60d31f7e9"  # 🔁 Replace with your key
BASE_URL = "http://ws.audioscrobbler.com/2.0/"
HEADERS = {"User-Agent": "LastFMFullInfo/1.0"}

def get_full_track_data(artist, track):
    def api_call(method, extra_params=None):
        params = {
            "method": method,
            "api_key": API_KEY,
            "artist": artist,
            "track": track,
            "format": "json"
        }
        if extra_params:
            params.update(extra_params)
        response = requests.get(BASE_URL, params=params, headers=HEADERS)
        return response.json()

    # 1. Track Info
    info = api_call("track.getInfo")
    track_info = info.get("track")
    if not track_info:
        return {"error": "Track not found on Last.fm."}

    # 2. Similar Tracks
    similar = api_call("track.getSimilar", {"limit": 5})
    similar_tracks = [s["name"] for s in similar.get("similartracks", {}).get("track", [])]

    # 3. Loved status (for a specific user — optional)
    # Uncomment and add your username if you want this:
    # loved = api_call("track.isLoved", {"user": "YOUR_USERNAME"})

    # 4. Build full JSON-style output
    output = {
        "track_name": track_info.get("name"),
        "artist": track_info.get("artist", {}).get("name"),
        "album": track_info.get("album", {}).get("title"),
        "duration_sec": int(track_info.get("duration", 0)) // 1000,
        "listeners": track_info.get("listeners"),
        "playcount": track_info.get("playcount"),
        "url": track_info.get("url"),
        "top_tags": [tag["name"] for tag in track_info.get("toptags", {}).get("tag", [])],
        "similar_tracks": similar_tracks
        # "loved_by_user": loved.get("loved")  # Only if user API is used
    }

    return output

# Example usage
full_data = get_full_track_data("BTS", "Dynamite")
print(json.dumps(full_data, indent=2))


# In[4]:


import requests
import json
import time

LASTFM_API_KEY = "da87e77d2348b4b9227b38b60d31f7e9"  # Replace with your Last.fm API key
HEADERS = {"User-Agent": "MetadataFusion/1.0"}
MB_BASE = "https://musicbrainz.org/ws/2"
LF_BASE = "http://ws.audioscrobbler.com/2.0/"

def search_artist_mb(artist_name):
    response = requests.get(f"{MB_BASE}/artist", params={"query": artist_name, "fmt": "json"}, headers=HEADERS)
    data = response.json()
    return data['artists'][0] if data['artists'] else None

def get_releases_mb(artist_id):
    response = requests.get(f"{MB_BASE}/release", params={"artist": artist_id, "fmt": "json", "limit": 3}, headers=HEADERS)
    return response.json().get('releases', [])

def get_recordings_mb(release_id):
    response = requests.get(f"{MB_BASE}/recording", params={"release": release_id, "fmt": "json", "limit": 20}, headers=HEADERS)
    return response.json().get('recordings', [])

def get_lastfm_track_info(artist, track):
    params = {
        "method": "track.getInfo",
        "api_key": LASTFM_API_KEY,
        "artist": artist,
        "track": track,
        "format": "json"
    }
    response = requests.get(LF_BASE, params=params, headers=HEADERS)
    data = response.json()
    return data.get("track")

def get_album_metadata(artist_name):
    artist = search_artist_mb(artist_name)
    if not artist:
        print("Artist not found.")
        return None

    releases = get_releases_mb(artist['id'])
    if not releases:
        print("No releases found.")
        return None

    selected_release = releases[0]
    recordings = get_recordings_mb(selected_release['id'])
    if not recordings:
        print("No tracks found.")
        return None

    all_track_data = {
        "artist": artist["name"],
        "album": selected_release["title"],
        "release_date": selected_release.get("date", "unknown"),
        "tracks": []
    }

    for track in recordings:
        time.sleep(1)  # Respect API limits
        track_data = get_lastfm_track_info(artist['name'], track['title'])
        if not track_data:
            print(f"Track not found on Last.fm: {track['title']}")
            continue

        all_track_data["tracks"].append({
            "track_name": track_data.get("name"),
            "duration_sec": int(track_data.get("duration", 0)) // 1000,
            "listeners": track_data.get("listeners"),
            "playcount": track_data.get("playcount"),
            "url": track_data.get("url"),
            "top_tags": [tag["name"] for tag in track_data.get("toptags", {}).get("tag", [])],
        })

    return all_track_data

# 🔧 Example usage
album_data = get_album_metadata("BTS")

if album_data:
    with open("full_album_metadata.json", "w", encoding="utf-8") as f:
        json.dump(album_data, f, indent=2, ensure_ascii=False)
    print("✅ Full album metadata saved to full_album_metadata.json")


# In[5]:


import requests
from bs4 import BeautifulSoup
import json
import time

# 🔑 Replace these
LASTFM_API_KEY = "da87e77d2348b4b9227b38b60d31f7e9"
GENIUS_TOKEN = "Bearer 15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO"

HEADERS_MB = {"User-Agent": "MetadataFusion/1.0"}
HEADERS_GENIUS = {"Authorization": GENIUS_TOKEN}
LF_BASE = "http://ws.audioscrobbler.com/2.0/"
MB_BASE = "https://musicbrainz.org/ws/2"

def get_musicbrainz_data(artist_name, track_name):
    # Search artist
    r = requests.get(f"{MB_BASE}/artist", params={"query": artist_name, "fmt": "json"}, headers=HEADERS_MB)
    artist_data = r.json().get("artists", [])[0]
    artist_id = artist_data['id']

    # Search recordings (tracks)
    rec_r = requests.get(f"{MB_BASE}/recording", params={
        "query": f'artist:{artist_name} AND recording:{track_name}',
        "fmt": "json",
        "limit": 1
    }, headers=HEADERS_MB)
    rec = rec_r.json().get("recordings", [{}])[0]

    return {
        "musicbrainz_id": rec.get("id"),
        "title": rec.get("title"),
        "artist": rec.get("artist-credit", [{}])[0].get("name", ""),
        "release_date": rec.get("first-release-date", "unknown"),
        "isrcs": rec.get("isrcs", [])
    }

def get_lastfm_data(artist, track):
    params = {
        "method": "track.getInfo",
        "api_key": LASTFM_API_KEY,
        "artist": artist,
        "track": track,
        "format": "json"
    }
    r = requests.get(LF_BASE, params=params)
    data = r.json().get("track")
    if not data:
        return {}

    return {
        "listeners": data.get("listeners"),
        "playcount": data.get("playcount"),
        "duration_sec": int(data.get("duration", 0)) // 1000,
        "top_tags": [t["name"] for t in data.get("toptags", {}).get("tag", [])],
        "url": data.get("url"),
        "similar_tracks": [s["name"] for s in data.get("similar", {}).get("track", [])]
    }

def search_genius(track, artist):
    search_url = f"https://api.genius.com/search"
    params = {"q": f"{track} {artist}"}
    r = requests.get(search_url, params=params, headers=HEADERS_GENIUS)
    hits = r.json().get("response", {}).get("hits", [])
    if not hits:
        return None
    song = hits[0]["result"]
    return song["url"]

def get_lyrics(genius_url):
    page = requests.get(genius_url)
    soup = BeautifulSoup(page.text, "html.parser")
    lyrics_div = soup.find("div", class_="Lyrics__Root-sc-1ynbvzw-0")
    if not lyrics_div:
        # Try fallback
        lyrics_div = soup.find("div", class_="lyrics")
    return lyrics_div.get_text(separator="\n").strip() if lyrics_div else "Lyrics not found."

def get_fused_metadata(artist, track):
    print("🔍 Getting MusicBrainz data...")
    mb_data = get_musicbrainz_data(artist, track)

    print("📈 Getting Last.fm data...")
    lf_data = get_lastfm_data(artist, track)
    time.sleep(1)

    print("🎤 Getting Genius data...")
    genius_url = search_genius(track, artist)
    lyrics = get_lyrics(genius_url) if genius_url else "Not found"

    combined = {
        "track": track,
        "artist": artist,
        "musicbrainz": mb_data,
        "lastfm": lf_data,
        "genius": {
            "genius_url": genius_url,
            "lyrics_excerpt": lyrics[:500] + "..." if lyrics else "N/A"
        }
    }
    return combined

# ✅ Try with BTS
result = get_fused_metadata("BTS", "Dynamite")

# 💾 Save as JSON
with open("full_track_metadata.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\n✅ Full metadata saved to full_track_metadata.json")


# In[10]:


import requests
import json
from bs4 import BeautifulSoup
import lyricsgenius
# 🔑 Replace these
LASTFM_API_KEY = "da87e77d2348b4b9227b38b60d31f7e9"
GENIUS_TOKEN = "Bearer 15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO"

genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
headers = {'User-Agent': 'MetadataAggregator/1.0 (example@example.com)'}

def get_musicbrainz_data(artist_name, track_title):
    # Search artist
    artist_url = f'https://musicbrainz.org/ws/2/artist/?query=artist:{artist_name}&fmt=json'
    artist_data = requests.get(artist_url, headers=headers).json()
    artist_id = artist_data['artists'][0]['id'] if artist_data['artists'] else None

    # Search recording
    recording_url = f'https://musicbrainz.org/ws/2/recording/?query=recording:{track_title}%20AND%20arid:{artist_id}&fmt=json'
    recording_data = requests.get(recording_url, headers=headers).json()

    if recording_data.get('recordings'):
        recording_info = recording_data['recordings'][0]
        release_group = recording_info.get('release_groups', [])
        release_dates = [release.get('first-release-date') for release in release_group]
        external_links = [link.get('url') for link in recording_info.get('relations', []) if link['type'] == 'website']
        
        return {
            "artist_id": artist_id,
            "recording": recording_info,
            "release_dates": release_dates,
            "external_links": external_links
        }
    return {}

def get_lastfm_data(artist_name, track_title):
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={LASTFM_API_KEY}&artist={artist_name}&track={track_title}&format=json"
    response = requests.get(url).json()

    track_info = response.get("track", {})
    tags = track_info.get('toptags', {}).get('tag', [])
    wiki = track_info.get('wiki', {})
    similar_tracks = track_info.get('similar', {}).get('track', [])

    return {
        "tags": tags,
        "wiki": wiki,
        "similar_tracks": similar_tracks
    }

def get_genius_data(artist_name, track_title):
    song = genius.search_song(track_title, artist=artist_name)
    if song:
        annotations = song.annotations if hasattr(song, 'annotations') else []
        release_date = song.release_date if hasattr(song, 'release_date') else "Unknown"
        artist_verified = song.artist_credits[0]['artist']['is_verified'] if hasattr(song, 'artist_credits') and song.artist_credits else False

        # Converting non-serializable Album object to string
        album = str(song.album) if song.album else "Unknown"

        return {
            "title": song.title,
            "artist": song.artist,
            "lyrics": song.lyrics,
            "url": song.url,
            "album": album,
            "release_date": release_date,
            "song_art_image_url": song.song_art_image_url,
            "annotations": annotations,
            "verified": artist_verified
        }
    return {}

def aggregate_metadata(artist_name, track_title):
    print(f"Fetching info for: {artist_name} - {track_title}")
    mb_data = get_musicbrainz_data(artist_name, track_title)
    lastfm_data = get_lastfm_data(artist_name, track_title)
    genius_data = get_genius_data(artist_name, track_title)

    combined_data = {
        "artist": artist_name,
        "track": track_title,
        "musicbrainz": mb_data,
        "lastfm": lastfm_data,
        "genius": genius_data
    }

    # Save as JSON
    with open("full_track_metadata_detailed.json", "w", encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)
    print("✅ Metadata saved to full_track_metadata_detailed.json")

# Example usage
aggregate_metadata("Coldplay", "Yellow")


# In[ ]:




