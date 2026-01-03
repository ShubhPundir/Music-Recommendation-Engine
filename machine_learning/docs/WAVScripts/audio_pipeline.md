## 🎶 Audio Download and Feature Insertion to Database

| Method Name | Description | Output Schema |
|-------------|-------------|----------------|
| `download_audio_to_memory(song_query)` | Downloads the best audio format for a given song query from YouTube and streams it into memory as a WAV file. | <details><summary>Click to view</summary> <pre>Returns a tuple:<br> (audio_data: io.BytesIO, title: str, channel: str, webpage_url: str)<br><br>Where:<br>  - audio_data: Audio data in memory (io.BytesIO)<br>  - title: Track title (str)<br>  - channel: Channel name (str)<br>  - webpage_url: Webpage URL (str)</pre></details> |
| `retry_on_connection_error(retries, delay)` | Decorator function to retry database operations in case of connection errors. | <details><summary>Click to view</summary> <pre>Returns the result of the wrapped function, retrying in case of connection errors</pre></details> |
| `insert_music_metadata(musicbrainz_id, track_title, channel, webpage_url)` | Inserts song metadata into the database under the specified table (`track_links`). | <details><summary>Click to view</summary> <pre>{<br>  "musicbrainz_id": str,<br>  "track_title": str,<br>  "channel": str,<br>  "webpage_url": str<br>}</pre></details> |
| `insert_to_db(data, table="audio_features")` | Inserts audio feature data into the database, flattening nested feature lists like `mfcc`, `spectral_contrast`, `chroma_cens`, and `tonnetz`. | <details><summary>Click to view</summary> <pre>{<br>  "musicbrainz_id": str,<br>  "duration_seconds": float,<br>  "sample_rate": int,<br>  "tempo": float,<br>  "loudness": float,<br>  "danceability": float,<br>  "energy": float,<br>  "speechiness": float,<br>  "acousticness": float,<br>  "instrumentalness": float,<br>  "liveness": float,<br>  "valence": float,<br>  "spectral_centroid": float,<br>  "spectral_rolloff": float,<br>  "spectral_bandwidth": float,<br>  "spectral_flatness": float,<br>  "zero_crossing_rate": float,<br>  "rms_energy": float,<br>  "tempo_variability": float,<br>  "f0_mean": float,<br>  "mel_mean": float,<br>  "dynamic_range": float,<br>  "mfcc_1": float,<br>  "mfcc_2": float,<br>  "mfcc_3": float,<br>  "mfcc_4": float,<br>  "mfcc_5": float,<br>  "mfcc_6": float,<br>  "mfcc_7": float,<br>  "mfcc_8": float,<br>  "mfcc_9": float,<br>  "mfcc_10": float,<br>  "mfcc_11": float,<br>  "mfcc_12": float,<br>  "mfcc_13": float,<br>  "spectral_contrast_1": float,<br>  "spectral_contrast_2": float,<br>  "spectral_contrast_3": float,<br>  "spectral_contrast_4": float,<br>  "spectral_contrast_5": float,<br>  "spectral_contrast_6": float,<br>  "spectral_contrast_7": float,<br>  "chroma_cens_1": float,<br>  "chroma_cens_2": float,<br>  "chroma_cens_3": float,<br>  "chroma_cens_4": float,<br>  "chroma_cens_5": float,<br>  "chroma_cens_6": float,<br>  "chroma_cens_7": float,<br>  "chroma_cens_8": float,<br>  "chroma_cens_9": float,<br>  "chroma_cens_10": float,<br>  "chroma_cens_11": float,<br>  "chroma_cens_12": float,<br>  "tonnetz_1": float,<br>  "tonnetz_2": float,<br>  "tonnetz_3": float,<br>  "tonnetz_4": float,<br>  "tonnetz_5": float,<br>  "tonnetz_6": float<br>}</pre></details> |

---

### CockroachDB `track_links` Table Schema

```sql
CREATE TABLE track_links (
    musicbrainz_id STRING PRIMARY KEY,
    track_title STRING,
    channel STRING,
    webpage_url STRING
);
```

```sql
CREATE TABLE audio_features (
    musicbrainz_id STRING PRIMARY KEY,
    duration_seconds FLOAT,
    sample_rate INT,
    tempo FLOAT,
    loudness FLOAT,
    danceability FLOAT,
    energy FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    spectral_centroid FLOAT,
    spectral_rolloff FLOAT,
    spectral_bandwidth FLOAT,
    spectral_flatness FLOAT,
    zero_crossing_rate FLOAT,
    rms_energy FLOAT,
    tempo_variability FLOAT,
    f0_mean FLOAT,
    mel_mean FLOAT,
    dynamic_range FLOAT,

    mfcc_1 FLOAT,
    mfcc_2 FLOAT,
    mfcc_3 FLOAT,
    mfcc_4 FLOAT,
    mfcc_5 FLOAT,
    mfcc_6 FLOAT,
    mfcc_7 FLOAT,
    mfcc_8 FLOAT,
    mfcc_9 FLOAT,
    mfcc_10 FLOAT,
    mfcc_11 FLOAT,
    mfcc_12 FLOAT,
    mfcc_13 FLOAT,

    spectral_contrast_1 FLOAT,
    spectral_contrast_2 FLOAT,
    spectral_contrast_3 FLOAT,
    spectral_contrast_4 FLOAT,
    spectral_contrast_5 FLOAT,
    spectral_contrast_6 FLOAT,
    spectral_contrast_7 FLOAT,

    chroma_cens_1 FLOAT,
    chroma_cens_2 FLOAT,
    chroma_cens_3 FLOAT,
    chroma_cens_4 FLOAT,
    chroma_cens_5 FLOAT,
    chroma_cens_6 FLOAT,
    chroma_cens_7 FLOAT,
    chroma_cens_8 FLOAT,
    chroma_cens_9 FLOAT,
    chroma_cens_10 FLOAT,
    chroma_cens_11 FLOAT,
    chroma_cens_12 FLOAT,

    tonnetz_1 FLOAT,
    tonnetz_2 FLOAT,
    tonnetz_3 FLOAT,
    tonnetz_4 FLOAT,
    tonnetz_5 FLOAT,
    tonnetz_6 FLOAT
);
```