## 🎶 Artist Data Loader and MongoDB Insertion Script

| Method Name | Description | Output Schema |
|-------------|-------------|----------------|
| `search_lastfm_artist(artist)` | Retrieves detailed artist metadata from Last.fm including tags, similar artists, and bio. (Used in the loader) | <details><summary>Click to view</summary> <pre>{<br>  "name": str,<br>  "tags": [str],<br>  "similar_artists": [<br>    {<br>      "name": str,<br>      "url": str<br>    }<br>  ],<br>  "wiki": {<br>    "published": str,<br>    "summary": str,<br>    "content": str<br>  }<br>}<br>or<br>{ "error": str }</pre></details> |
| `get_artist_id_musicbrainz(artist_name)` | Retrieves the MusicBrainz artist ID for a given artist. | <details><summary>Click to view</summary> <pre>{<br>  "musicbrainz_id": str (or None)<br>}</pre></details> |
| CSV Loader & MongoDB Insert | Loads artist data from a CSV file, calls `search_lastfm_artist` and `get_artist_id_musicbrainz`, and inserts results into MongoDB. | <details><summary>Click to view</summary> <pre>{<br>  "artist": str,<br>  "data": {<br>    "name": str,<br>    "tags": [str],<br>    "similar_artists": [<br>      {<br>        "name": str,<br>        "url": str<br>      }<br>    ],<br>    "wiki": {<br>      "published": str,<br>      "summary": str,<br>      "content": str<br>    },<br>    "musicbrainz_id": str<br>  },<br>  "_id": ObjectId<br>}<br>or<br>{ "error": str } </pre></details> |

---

### CSV Loader Workflow
1. **Input:** Reads artist data from a CSV file (`Albums - Sheet2.csv`).
2. **Output:** MongoDB document insertion, or skip if no data is returned.

The MongoDB document will have the following structure:

```json
{
  "_id": ObjectId,
  "name": "Artist Name",
  "tags": ["rock", "pop"],
  "similar_artists": [
    {
      "name": "Similar Artist 1",
      "url": "https://last.fm/artist-url"
    }
  ],
  "wiki": {
    "published": "YYYY-MM-DD",
    "summary": "Artist summary from Last.fm",
    "content": "Full bio content from Last.fm"
  },
  "musicbrainz_id": "12345"  // or null if not available
}
```