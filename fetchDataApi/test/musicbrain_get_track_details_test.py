from musicbrainz import get_track_details_musicbrainz
from pprint import pprint

x = get_track_details_musicbrainz("01564f1c-99b2-466a-a60d-4e22a5008525")
pprint(x)