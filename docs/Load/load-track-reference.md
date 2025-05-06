## 🎶 MusicBrainz Track Details Fetch and Insert to CockroachDB

| Method Name | Description | Output Schema |
|-------------|-------------|----------------|
| `fetch_musicbrainz_ids()` | Fetches all `musicbrainz_id` values from the `lyrics` table in CockroachDB. | <details><summary>Click to view</summary> <pre>[<br>  "musicbrainz_id_1",<br>  "musicbrainz_id_2",<br>  "musicbrainz_id_3",<br>  ...<br>]</pre></details> |
| `insert_track_details(track_data)` | Inserts detailed track information into the `track_reference` table in CockroachDB. | <details><summary>Click to view</summary> <pre>{<br>  "musicbrainz_id": str,<br>  "title": str,<br>  "artist": str,<br>  "artist_id": str,<br>  "album": str,<br>  "album_id": str,<br>  "release_date": str,<br>  "country": str,<br>  "length": int<br>}</pre></details> |
| `process_musicbrainz_ids(musicbrainz_ids)` | Fetches detailed track information for a list of `musicbrainz_id` values from MusicBrainz, and inserts the data into CockroachDB. | <details><summary>Click to view</summary> <pre>{<br>  "track_data": {<br>    "musicbrainz_id": str,<br>    "title": str,<br>    "artist": str,<br>    "artist_id": str,<br>    "album": str,<br>    "album_id": str,<br>    "release_date": str,<br>    "country": str,<br>    "length": int<br>  },<br>  "error": (optional) str<br>}</pre></details> |

---

### CockroachDB `track_reference` Table Schema

```sql
CREATE TABLE track_reference (
    musicbrainz_id STRING PRIMARY KEY,
    title STRING,
    artist STRING,
    artist_id STRING,
    album STRING,
    album_id STRING,
    release_date STRING,
    country STRING,
    length INT8  -- Track length in milliseconds
);
```