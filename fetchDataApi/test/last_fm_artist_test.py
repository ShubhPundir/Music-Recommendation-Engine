from last_fm import search_lastfm_artist
from pprint import pprint

data = search_lastfm_artist("The Beatles")
pprint(data)