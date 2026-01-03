## 🎶 Track Metadata and Lyrics Insertion with CockroachDB and MongoDB

| Method Name | Description | Output Schema |
|-------------|-------------|----------------|
| `insert_lyrics_into_cockroach(lyrics_data)` | Inserts lyrics data (Genius lyrics, Last.fm wiki summary, and content) into CockroachDB for a track. | <details><summary>Click to view</summary> <pre>{<br>  "musicbrainz_id": str,<br>  "genius_lyrics": str,<br>  "genius_url": str,<br>  "lastfm_wiki_summary": str,<br>  "lastfm_wiki_content": str<br>}</pre></details> |
| `process_track(artist_name, album_name, track_name)` | Fetches track metadata and lyrics for a given artist, album, and track, and inserts the data into CockroachDB and MongoDB. | <details><summary>Click to view</summary> <pre>{<br>  "artist": str,<br>  "track": str,<br>  "album": str,<br>  "metadata": {<br>    "track_data": {<br>      "musicbrainz_id": str,<br>      "other_metadata": str<br>    },<br>    "lyrics_data": {<br>      "genius_lyrics": str,<br>      "genius_url": str,<br>      "lastfm_wiki_summary": str,<br>      "lastfm_wiki_content": str<br>    }<br>  }<br>}</pre></details> |
| `stream_albums_in_batches(batch_size)` | Streams albums in batches from MongoDB for processing. | <details><summary>Click to view</summary> <pre>[ {<br>  "artist": str,<br>  "name": str,<br>  "tracks": [<br>    {<br>      "name": str,<br>      "duration": int,<br>      "url": str<br>    }<br>  ]<br> } ]</pre></details> |

---

### MongoDB and CockroachDB Schema

#### MongoDB `track_metadata` Collection:

```json
{
  "_id": ObjectId,
  "artist": "Artist Name",
  "track": "Track Name",
  "album": "Album Name",
  "metadata": {
    "track_data": {
      "musicbrainz_id": "MBID",
      "other_metadata": "Additional metadata if applicable"
    },
    "lyrics_data": {
      "genius_lyrics": "Lyrics from Genius",
      "genius_url": "Genius URL for lyrics",
      "lastfm_wiki_summary": "Summary from Last.fm wiki",
      "lastfm_wiki_content": "Full content from Last.fm wiki"
    }
  }
}
```

CREATE TABLE lyrics (
    musicbrainz_id STRING PRIMARY KEY,
    genius_lyrics TEXT,
    genius_url STRING,
    lastfm_wiki_summary TEXT,
    lastfm_wiki_content TEXT
);
