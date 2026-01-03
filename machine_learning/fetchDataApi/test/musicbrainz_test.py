from musicbrainz import get_artist_id_musicbrainz

from pprint import pprint

data = get_artist_id_musicbrainz(artist_name="Coldplay")
pprint(data)
