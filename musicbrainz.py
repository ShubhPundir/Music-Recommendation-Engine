#!/usr/bin/env python
# coding: utf-8

# In[54]:


pip install requests


# In[55]:


import requests

def search_artist(artist_name):
    base_url = "https://musicbrainz.org/ws/2/artist/"
    headers = {
        "User-Agent": "MusicInfoFetcher/1.0 ( your-email@example.com )"  # Replace with your email
    }
    params = {
        "query": artist_name,
        "fmt": "json"
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
artist_name = "Coldplay"
info = search_artist(artist_name)

if info:
    for artist in info.get("artists", []):
        print(f"Name: {artist['name']}, ID: {artist['id']}, Country: {artist.get('country')}")


# In[49]:


import requests

BASE_URL = "https://musicbrainz.org/ws/2/"

def get_artist_info(artist_name):
    headers = {
        "User-Agent": "MusicInfoFetcher/1.0 (contact@email.com)"  # Replace with your contact email
    }
    params = {
        "query": f'artist:"{artist_name}"',
        "fmt": "json"
    }

    response = requests.get(BASE_URL + "artist/", params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "artists" in data and data["artists"]:
            artist = data["artists"][0]  # Taking the first result
            
            print(f"🎤 Artist: {artist['name']}")
            print(f"📌 Country: {artist.get('country', 'Unknown')}")
            print(f"📅 Begin Date: {artist.get('life-span', {}).get('begin', 'Unknown')}")
            print(f"📅 End Date: {artist.get('life-span', {}).get('end', 'Still active')}")
            print(f"🔗 MusicBrainz URL: https://musicbrainz.org/artist/{artist['id']}")
        else:
            print("Artist not found.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Example usage
get_artist_info("bts")


# In[56]:


get_artist_info("Taylor Swift")   # Full name
get_artist_info("Justin Bieber")            # Korean name
get_artist_info("BTS")             # Group name


# In[51]:


import requests

def get_artist_mbid(artist_name):
    url = f"https://musicbrainz.org/ws/2/artist/?query={artist_name}&fmt=json"
    headers = {"User-Agent": "MusicBrainz-DataFetcher/1.0 (your_email@example.com)"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Error fetching data."

    data = response.json()
    if "artists" in data and data["artists"]:
        artist = data["artists"][0]  # Take the first result
        return {
            "Name": artist["name"],
            "MBID": artist["id"],
            "Country": artist.get("country", "Unknown"),
            "Type": artist.get("type", "Unknown"),
            "Disambiguation": artist.get("disambiguation", "N/A")
        }
    return "Artist not found."

print(get_artist_mbid("Taylor Swift"))


# In[53]:


def get_track_isrc(track_name):
    url = f"https://musicbrainz.org/ws/2/recording/?query={track_name}&fmt=json"
    headers = {"User-Agent": "MusicBrainz-DataFetcher/1.0 (your_email@example.com)"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Error fetching track data."

    data = response.json()
    if "recordings" in data and data["recordings"]:
        track = data["recordings"][0]  # First result
        return {
            "Title": track["title"],
            "Artist": track["artist-credit"][0]["name"],
            "ISRC": track.get("isrcs", ["No ISRC found"])[0]
        }
    return "Track not found."

print(get_track_isrc("Seven Jungkook"))


# In[58]:


import requests

def get_artist_details(artist_id):
    url = f"https://musicbrainz.org/ws/2/artist/{artist_id}"
    headers = {
        "User-Agent": "MusicInfoFetcher/1.0 (your-email@example.com)"
    }
    params = {
        "fmt": "json",
        "inc": "aliases+tags+ratings+genres"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching artist details: {response.status_code}")
        return None

# Example: Coldplay's ID (from search)
coldplay_id = "cc197bad-dc9c-440d-a5b5-d52ba2e14234"
details = get_artist_details(coldplay_id)

if details:
    print("Name:", details.get("name"))
    print("Country:", details.get("country"))
    print("Disambiguation:", details.get("disambiguation"))
    
    print("\nGenres:")
    for genre in details.get("genres", []):
        print("-", genre.get("name"))

    print("\nTags:")
    for tag in details.get("tags", []):
        print("-", tag.get("name"))

    print("\nAliases:")
    for alias in details.get("aliases", []):
        print("-", alias.get("name"))


# In[64]:


import requests

def get_albums_by_artist(artist_id, limit=10):
    url = "https://musicbrainz.org/ws/2/release"
    headers = {
        "User-Agent": "MusicFetcherApp/1.0 (your-email@example.com)"
    }
    params = {
        "artist": artist_id,
        "fmt": "json",
        "limit": limit,
        "inc": "release-groups"  # includes album-level info
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        releases = response.json().get('releases', [])
        for release in releases:
            print(f"Title: {release.get('title')}")
            print(f"Release Date: {release.get('date')}")
            print(f"Release ID: {release.get('id')}")
            print("---")
    else:
        print("Error:", response.status_code)

# Coldplay artist ID
coldplay_id = "cc197bad-dc9c-440d-a5b5-d52ba2e14234"
get_albums_by_artist(coldplay_id)



# In[67]:


def get_songs_from_album(release_id):
    url = f"https://musicbrainz.org/ws/2/release/{release_id}"
    headers = {
        "User-Agent": "MusicFetcherApp/1.0 (your-email@example.com)"
    }
    params = {
        "fmt": "json",
        "inc": "recordings"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        media = response.json().get('media', [])
        for disc in media:
            for track in disc.get('tracks', []):
                print(f"{track.get('number')}. {track.get('title')} ({track.get('length')} ms)")
    else:
        print("Error:", response.status_code)

get_songs_from_album("a7d5b6ba-6cda-35e8-a6ca-e95113533f46")


# In[68]:


import requests

def get_full_artist_info(artist_id):
    url = f"https://musicbrainz.org/ws/2/artist/{artist_id}"
    headers = {
        "User-Agent": "MusicInfoExplorer/1.0 (your-email@example.com)"
    }
    params = {
        "fmt": "json",
        "inc": "aliases+tags+ratings+genres+artist-rels+label-rels+url-rels"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    data = response.json()

    print(f"\n🎤 Artist Name: {data.get('name')}")
    print(f"🆔 ID: {data.get('id')}")
    print(f"🌍 Country: {data.get('country')}")
    print(f"📆 Begin Date: {data.get('life-span', {}).get('begin')}")
    print(f"📆 End Date: {data.get('life-span', {}).get('end')}")
    print(f"📝 Disambiguation: {data.get('disambiguation')}")
    print(f"👥 Type: {data.get('type')}")
    
    print("\n🎭 Aliases:")
    for alias in data.get("aliases", []):
        print(f" - {alias.get('name')} ({alias.get('locale', 'N/A')})")

    print("\n🎶 Genres:")
    for genre in data.get("genres", []):
        print(f" - {genre.get('name')}")

    print("\n🏷️ Tags:")
    for tag in data.get("tags", []):
        print(f" - {tag.get('name')}")

    print("\n⭐ Rating:")
    rating = data.get("rating", {})
    print(f" - Score: {rating.get('value')} ({rating.get('votes-count')} votes)")

    print("\n🔗 Related URLs:")
    for rel in data.get("relations", []):
        if rel.get("type") == "official homepage" or rel.get("type") == "wikipedia" or rel.get("type") == "social network":
            print(f" - {rel.get('type')}: {rel.get('url', {}).get('resource')}")

    print("\n👥 Artist Relationships:")
    for rel in data.get("relations", []):
        if rel.get("type") in ["member of band", "collaboration"]:
            related_artist = rel.get("artist", {}).get("name")
            role = rel.get("type")
            begin = rel.get("begin")
            end = rel.get("end")
            print(f" - {related_artist} ({role}, {begin or 'start'} - {end or 'present'})")

    print("\n💽 Label Relationships:")
    for rel in data.get("relations", []):
        if rel.get("type") == "label":
            label = rel.get("label", {}).get("name")
            begin = rel.get("begin")
            end = rel.get("end")
            print(f" - {label} ({begin or 'start'} - {end or 'present'})")

# Example: Coldplay
coldplay_id = "cc197bad-dc9c-440d-a5b5-d52ba2e14234"
get_full_artist_info(coldplay_id)


# In[ ]:




