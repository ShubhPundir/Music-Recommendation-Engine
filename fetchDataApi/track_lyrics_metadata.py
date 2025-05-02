import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
## ensures that fetchDataApi is not searched within the listing of python modules, but our root directories, WOW LOL
from fetchDataApi.last_fm import search_lastfm_track
from fetchDataApi.musicbrainz import search_musicbrainz
from fetchDataApi.genius import search_genius
# from pprint import pprint

def get_track_lyrics_metadata(artist, track):
    musicbrainz_data = search_musicbrainz(artist, track)
    lastfm_data = search_lastfm_track(artist, track)
    genius_data = search_genius(artist, track)

    track_metadata = {
        "prompted_artist": artist,
        "prompted_track": track,
        "musicbrainz": musicbrainz_data,
        "lastfm": lastfm_data,
        "genius": genius_data
    }
    track_metadata["genius"].pop('lyrics')
    track_metadata["genius"].pop('url')
    track_metadata["lastfm"].pop('wiki')


    lyrics_data = {
        "musicbrainz_id": musicbrainz_data.get("recording_id"),
        "genius_lyrics": genius_data.get("lyrics"),
        "genius_url": genius_data.get("url"),
        "lastfm_wiki_summary": lastfm_data.get("wiki", {}).get("summary"),
        "lastfm_wiki_content": lastfm_data.get("wiki", {}).get("content")
    }

    return track_metadata, lyrics_data

# x,y = get_track_lyrics_metadata("The Beatles", "Chains")
# pprint(x)

# print("-----"*10,"\n")
# pprint(y)