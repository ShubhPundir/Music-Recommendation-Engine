import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")


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


# print(search_genius("The Beatles", "All my loving"))