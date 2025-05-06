## 🎶 CSV Loader and MongoDB Insertion Script

| Method Name | Description | Output Schema |
|-------------|-------------|----------------|
| `search_lastfm_album(artist, album)` | Retrieves detailed album metadata from Last.fm including tracklist, tags, images, and wiki summary. (Used in the loader) | <details><summary>Click to view</summary> <pre>{<br>  "name": str,<br>  "artist": str,<br>  "url": str,<br>  "playcount": str,<br>  "listeners": str,<br>  "tags": [str],<br>  "images": {<br>    size: str (image URL)<br>  },<br>  "tracks": [<br>    {<br>      "name": str,<br>      "duration": int,<br>      "rank": int,<br>      "url": str,<br>      "artist": str<br>    }<br>  ],<br>  "wiki_summary": str<br>}<br>or<br>None / printed {"error": str}</pre></details> |
| CSV Loader & MongoDB Insert | Loads album data from a CSV file, calls `search_lastfm_album`, and inserts results into MongoDB. | <details><summary>Click to view</summary> <pre>{<br>  "album": str,<br>  "artist": str,<br>  "data": {<br>    "name": str,<br>    "artist": str,<br>    "url": str,<br>    "playcount": str,<br>    "listeners": str,<br>    "tags": [str],<br>    "images": {<br>      size: str (image URL)<br>    },<br>    "tracks": [<br>      {<br>        "name": str,<br>        "duration": int,<br>        "rank": int,<br>        "url": str,<br>        "artist": str<br>      }<br>    ],<br>    "wiki_summary": str<br>  },<br>  "_id": ObjectId<br>}<br>or<br>{ "error": str } </pre></details> |

---

### CSV Loader Workflow
1. **Input:** Reads album and artist data from a CSV file (`Albums - Sheet2.csv`).
2. **Output:** MongoDB document insertion, or skip if no data is returned.

The MongoDB document will have the following structure:

```json
{
  "_id": ObjectId,
  "name": "Album Name",
  "artist": "Artist Name",
  "url": "https://last.fm/album-url",
  "playcount": "12345",
  "listeners": "67890",
  "tags": ["rock", "pop"],
  "images": {
    "small": "https://image.url/small.jpg",
    "medium": "https://image.url/medium.jpg",
    "large": "https://image.url/large.jpg"
  },
  "tracks": [
    {
      "name": "Track Name",
      "duration": 240,
      "rank": 1,
      "url": "https://last.fm/track-url",
      "artist": "Track Artist"
    }
  ],
  "wiki_summary": "Album summary from Last.fm"
}
