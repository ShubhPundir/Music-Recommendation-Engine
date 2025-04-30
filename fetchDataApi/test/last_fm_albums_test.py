from last_fm import search_lastfm_album
from pprint import pprint

data = search_lastfm_album(album="EUROPA", artist="SZA")
pprint(data)


## I don't know why I can't reference last_fm, just shift this file to a .. directory
## OR
## have it in the same folder as last_fm.py