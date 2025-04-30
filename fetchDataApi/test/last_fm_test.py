from last_fm import search_lastfm_album, search_lastfm_track
from pprint import pprint

data = search_lastfm_album(album="EUROPA", artist="SZA")
pprint(data)