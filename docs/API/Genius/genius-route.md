# 🎤 Genius Lyrics Fetching API Documentation

This document outlines how the `search_genius` function fetches song metadata and lyrics using the Genius API and web scraping.

---

## 🔧 Setup & Environment

### 📁 Environment Variable:
- **GENIUS_ACCESS_TOKEN**  
  Stored in a `.env` file and loaded via `dotenv`.

```env
GENIUS_ACCESS_TOKEN=your_genius_api_access_token_here
```

### Headers
```python
headers = {
    "Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"
}
```
## 🎤 Genius API Integration Methods

| Method Name | Description | Output Schema |
|-------------|-------------|----------------|
| `search_genius(artist, track)` | Searches for a song using artist and track name, retrieves metadata and lyrics by scraping the Genius song page. | <details><summary>Click to view</summary> <pre>{<br>  "title": str,<br>  "artist": str,<br>  "lyrics": str,<br>  "url": str,<br>  "album": str,<br>  "release_date": str,<br>  "song_art_image_url": str,<br>  "verified": bool<br>}<br>or<br>{ "error": str }</pre> </details> |
| `scrape_lyrics(url)` | Scrapes the Genius song webpage to extract the lyrics from HTML containers. | <details><summary>Click to view</summary> <pre>str (lyrics text)<br>or<br>str (error message)</pre> </details> |
