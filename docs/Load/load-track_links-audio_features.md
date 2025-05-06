## 🎧 Audio Feature Extraction Pipeline (YouTube → WAV Buffer → Analysis → CockroachDB)

| Method | Description | Output Schema |
|--------|-------------|----------------|
| `fetch_musicbrainz_ids()` | Fetches `(musicbrainz_id, title, artist)` from the `track_reference` table in CockroachDB. | <details><summary>Click to view</summary><pre>[<br>  ("musicbrainz_id_1", "Title 1", "Artist 1"),<br>  ("musicbrainz_id_2", "Title 2", "Artist 2"),<br>  ...<br>]</pre></details> |
| `download_audio_to_memory(query)` | Downloads audio from YouTube matching the query `"{title} {artist}"`. Returns in-memory WAV buffer + metadata. | <details><summary>Click to view</summary><pre>(<br>  BytesIO,   # audio buffer in WAV format<br>  str,       # YouTube title<br>  str,       # Channel name<br>  str        # YouTube URL<br>)</pre></details> |
| `insert_music_metadata()` | Inserts YouTube metadata into a dedicated table (e.g. `track_metadata`). | <details><summary>Click to view</summary><pre>{<br>  "musicbrainz_id": str,<br>  "title": str,<br>  "channel": str,<br>  "url": str<br>}</pre></details> |
| `extract_audio_features_from_buffer()` | Analyzes audio buffer and returns extracted features (tempo, key, etc.). | <details><summary>Click to view</summary><pre>{<br>  "tempo": float,<br>  "duration": float,<br>  "rms": float,<br>  "zero_crossing_rate": float,<br>  "spectral_centroid": float,<br>  ...<br>  "musicbrainz_id": str<br>}</pre></details> |
| `insert_to_db(features)` | Inserts extracted features into a table (e.g. `audio_features`). | Same as above |
| `chunks(lst, BATCH_SIZE)` | Splits the list of tracks into batches of configurable size. | `Iterator[List[Tuple[str, str, str]]]` |

---

### ✅ Final Output Tables in CockroachDB

1. **`track_metadata`**:
   ```sql
   musicbrainz_id TEXT PRIMARY KEY,
   title TEXT,
   channel TEXT,
   url TEXT


2. 

musicbrainz_id TEXT PRIMARY KEY,
tempo FLOAT,
duration FLOAT,
rms FLOAT,
zero_crossing_rate FLOAT,
spectral_centroid FLOAT,
...

