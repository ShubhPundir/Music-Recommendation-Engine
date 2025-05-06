## 🎵 MusicBrainz API Integration Methods

| Method Name | Description | Output Schema |
|-------------|-------------|----------------|
| `search_musicbrainz(artist, track)` | Searches for a song by artist and track name. Returns metadata such as title, artist, album, release date, and country. | `{ recording_id: str, title: str, artist: str, artist_id: str, album: str, album_id: str, release_date: str, country: str, length: int }` or `{ error: str }` |
| `get_artist_id_musicbrainz(artist_name)` | Retrieves the MusicBrainz Artist ID for a given artist name. Prioritizes exact matches. | `str (artist_id)` or `None` |
| `get_album_tracks_musicbrainz(artist_name, album_name)` | Fetches a list of track titles from a specified album by an artist using release group and release lookups. | `List[str]` |
| `get_track_details_musicbrainz(recording_id)` | Fetches detailed metadata about a recording using its MusicBrainz recording ID, including normalized release date and country. | `{ recording_id: str, title: str, artist: str, artist_id: str, album: str, album_id: str, release_date: str or None, country: str, length: int }` or `{ error: str }` |
