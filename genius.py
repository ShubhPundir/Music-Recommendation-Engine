#!/usr/bin/env python
# coding: utf-8

# In[1]:


headers = {
    "Authorization": "15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO"
}


# In[2]:


import requests

headers = {"Authorization": "15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO"}
test = requests.get("https://api.genius.com/songs/2342329", headers=headers)

print(test.status_code)
print(test.json())


# In[5]:


import requests
from bs4 import BeautifulSoup
import json
import time

ACCESS_TOKEN = '15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO'  # <-- Replace with yours

BASE_URL = "https://api.genius.com"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


# In[57]:


import requests
from bs4 import BeautifulSoup
import re

def get_clean_song_titles():
    url = 'https://genius.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    raw_titles = []
    for tag in soup.select('a[href*="-lyrics"]'):
        text = tag.get_text(strip=True)
        raw_titles.append(text)

    clean_titles = []
    for t in raw_titles:
        # Remove view counts (like "1.2M", "321.4K", etc.)
        t = re.sub(r'\d+\.\d+[MK]', '', t)
        # Remove "Lyrics"
        t = re.sub(r'Lyrics', '', t, flags=re.IGNORECASE)
        # Remove any digits or ranks at start
        t = re.sub(r'^\d+', '', t)
        # Remove artist names if possible (this is not perfect)
        t = re.sub(r'by\s.*', '', t, flags=re.IGNORECASE)
        clean_titles.append(t.strip())

    return clean_titles[:10]  # limit to top 10

# Usage
titles = get_clean_song_titles()
print(titles)


# In[25]:


def search_song_id(title):
    search_url = f"{BASE_URL}/search"
    params = {"q": title}
    response = requests.get(search_url, params=params, headers=headers)
    data = response.json()
    hits = data['response']['hits']
    if hits:
        return hits[0]['result']['id']
    return None


# In[26]:


def get_song_info(song_id):
    song_url = f"{BASE_URL}/songs/{song_id}"
    response = requests.get(song_url, headers=headers)
    return response.json()


# In[27]:


song_titles = [
    "Creep by Radiohead",
    "Love Yourself by Justin Bieber",
    "You'll Be In My Heart by Phil Collins",
    "Not Like Us by Kendrick Lamar"
]


# In[28]:


song_metadata = []

for title in song_titles:
    print(f"Searching for: {title}")
    song_id = search_song_id(title)
    if song_id:
        metadata = get_song_info(song_id)
        song_metadata.append(metadata)
        print(f"✓ Got metadata for {title}")
    else:
        print(f"✗ Couldn't find ID for: {title}")
    time.sleep(1)


# In[52]:


with open("genius_top_songs.json", "w") as f:
    json.dump(song_metadata, f, indent=2)


# In[35]:


from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file into the environment
genius_access_token = os.getenv('15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO')


# In[36]:


import os
os.environ['GENIUS_ACCESS_TOKEN'] = '15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO'


# In[37]:


import lyricsgenius

# Initialize Genius API client
genius = lyricsgenius.Genius(os.getenv('GENIUS_ACCESS_TOKEN'))


# In[38]:


artist_name = "BTS"
artist = genius.search_artist(artist_name, max_songs=5)


# In[39]:


album_name = "1989"
artist_name = "Taylor Swift"

# Standard edition tracklist
tracklist = [
    "Welcome to New York",
    "Blank Space",
    "Style",
    "Out of the Woods",
    "All You Had to Do Was Stay",
    "Shake It Off"
]


# In[40]:


for track in tracklist:
    song = genius.search_song(track, artist_name)
    if song:
        print(f"Lyrics for '{track}':\n{song.lyrics}\n")
    else:
        print(f"Lyrics for '{track}' not found.\n")


# In[41]:


import requests

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer 15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO'}

search_query = "Taylor Swift 1989"
search_url = f"{base_url}/search?q={search_query}"

response = requests.get(search_url, headers=headers)
data = response.json()


# In[42]:


songs = data['response']['hits']
for song in songs:
    song_info = song['result']
    song_title = song_info['title']
    song_id = song_info['id']
    song_url = song_info['url']
    song_release_date = song_info.get('release_date', 'N/A')
    song_pageviews = song_info['stats'].get('pageviews', 'N/A')

    print(f"Title: {song_title}")
    print(f"Release Date: {song_release_date}")
    print(f"Page Views: {song_pageviews}")
    print(f"URL: {song_url}\n")


# In[43]:


from bs4 import BeautifulSoup
import requests

album_url = "https://genius.com/albums/Taylor-swift/1989"
response = requests.get(album_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract album release date
release_date = soup.find('span', class_='metadata_unit-info').text.strip()
print(f"Release Date: {release_date}")

# Extract track titles
tracks = soup.find_all('h3', class_='chart_row-content-title')
for track in tracks:
    track_title = track.text.strip()
    print(f"Track: {track_title}")


# In[44]:


album = genius.search_album("1989", "Taylor Swift")


# In[45]:


import requests
import json
import time

# Your Genius API token
ACCESS_TOKEN = '15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO'
BASE_URL = "https://api.genius.com"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Function to search and get song IDs
def search_songs(query, max_results=5):
    search_url = f"{BASE_URL}/search"
    params = {'q': query}
    response = requests.get(search_url, params=params, headers=headers)
    data = response.json()
    
    song_ids = []
    for hit in data['response']['hits'][:max_results]:
        song_id = hit['result']['id']
        song_ids.append(song_id)
    
    return song_ids
# Function to get song details
def get_song_info(song_id):
    song_url = f"{BASE_URL}/songs/{song_id}"
    response = requests.get(song_url, headers=headers)
    return response.json()

# Example usage
search_queries = ["Taylor Swift", "Eminem", "Billie Eilish", "Adele", "Coldplay"]
all_song_data = []

for query in search_queries:
    print(f"Searching for songs by: {query}")
    ids = search_songs(query)
    for song_id in ids:
        song_data = get_song_info(song_id)
        all_song_data.append(song_data)
        print(f"Fetched song ID: {song_id}")
        time.sleep(1)  # To avoid hitting rate limits

# Optional: Save to JSON file
with open("genius_songs_data.json", "w") as f:
    json.dump(all_song_data, f, indent=2)


# In[46]:


def get_artist_songs(artist_id, max_songs=20):
    songs = []
    page = 1

    while len(songs) < max_songs:
        url = f"{BASE_URL}/artists/{artist_id}/songs"
        params = {"page": page, "per_page": 10}
        response = requests.get(url, headers=headers, params=params).json()
        
        if not response['response']['songs']:
            break

        for song in response['response']['songs']:
            songs.append(song['id'])
            if len(songs) >= max_songs:
                break

        page += 1
        time.sleep(1)  # To avoid rate limits
    
    return songs

# Example: Justin Bieber's ID is 357
bieber_song_ids = get_artist_songs(artist_id=357, max_songs=15)
# Now get song details
bieber_data = []
for song_id in bieber_song_ids:
    song_data = get_song_info(song_id)
    bieber_data.append(song_data)
    print(f"Fetched song ID: {song_id}")


# In[47]:


import requests
import random

# Replace with your Genius API Access Token
ACCESS_TOKEN = "15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO"

# Base URL for Genius API
BASE_URL = "https://api.genius.com"

# Headers for authorization
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Function to search for songs
def search_random_songs():
    query = random.choice(["love", "night", "dream", "fire", "star"])  # Random search keyword
    search_url = f"{BASE_URL}/search?q={query}"
    response = requests.get(search_url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        hits = data["response"]["hits"]
        songs = random.sample(hits, min(5, len(hits)))  # Pick up to 5 random songs
        print("🎵 Here are 5 random songs from Genius API:")
        for i, song in enumerate(songs, start=1):
            title = song["result"]["title"]
            artist = song["result"]["primary_artist"]["name"]
            url = song["result"]["url"]
            print(f"{i}. {title} by {artist} → {url}")
    else:
        print(f"Error: {response.status_code}, {response.json()}")

# Run the function
search_random_songs()


# In[48]:


import requests

def search_song(song_name):
    headers = {"Authorization": "Bearer KFe53Rk-6NzSke1n4yCPCxdFmRE6cf7VtkngFgaMToq7n1JE36p1iSqCxrKazZ92"}
    url = f"https://api.genius.com/search?q={song_name}"
    response = requests.get(url, headers=headers).json()
    
    if 'response' in response and 'hits' in response['response'] and response['response']['hits']:
        return response['response']['hits'][0]['result']  # First result
    else:
        return None  # Song not found

song_info = search_song("Love Yourself")
if song_info:
    print(f"🎵 Song: {song_info['title']}")
    print(f"🎤 Artist: {song_info['primary_artist']['name']}")
    print(f"🔗 Genius URL: {song_info['url']}")
else:
    print("❌ Song not found.")


# In[49]:


search_song("Justin Bieber Love Yourself")


# In[50]:


search_song("Taylor Swift Cruel Summer")
search_song("Drake God's Plan")
search_song("The Weeknd Blinding Lights")
search_song("Adele Easy On Me")
search_song("Dua Lipa Levitating")
search_song("Billie Eilish What Was I Made For?")
search_song("Post Malone Circles")
search_song("Olivia Rodrigo vampire")
search_song("Harry Styles As It Was")
search_song("Travis Scott FE!N")


# In[ ]:




