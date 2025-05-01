from musicbrainz import search_musicbrainz, get_album_tracks_musicbrainz
from last_fm import search_lastfm_track
from genius import search_genius
import json

def get_song_metadata(artist, track):
    return {
        "prompted_artist": artist,
        "prompted_track": track,
        "musicbrainz": search_musicbrainz(artist, track),
        "lastfm": search_lastfm_track(artist, track),
        "genius": search_genius(artist, track)
    }

def compile_album(artist, album):
    tracks = get_album_tracks_musicbrainz(artist_name=artist, album_name=album)
    print(f"Compiling {tracks} in album: {album} by {artist}")
    print(f"Number of tracks: {len(tracks)}")



print("-------"*15)

prompted_artist = "The Beatles"
prompted_track = "A Hard Day's Night"
prompted_album = "Please Please Me"

# compile_album(prompted_artist, prompted_album)

metadata = get_song_metadata(prompted_artist, prompted_track)

print("\n🎧 Song Metadata:\n")
print(json.dumps(metadata, indent=4, ensure_ascii=False))

filename = f"{prompted_artist}_{prompted_track}_metadata.json".replace(" ", "_")
with open(filename, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4, ensure_ascii=False)

print(f"\n✅ Metadata saved to '{filename}'")