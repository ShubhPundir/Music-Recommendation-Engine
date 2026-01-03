import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongodb import db
from database.cockroachdb import get_cockroach_connection

# MongoDB setup
track_metadata_collection = db['temp_tracks_metadata']

# Load CockroachDB musicbrainz_ids into a set
conn = get_cockroach_connection()
crdb_ids = set()
with conn.cursor() as cursor:
    cursor.execute("SELECT musicbrainz_id FROM lyrics;")
    crdb_ids.update(str(row[0]).strip() for row in cursor.fetchall())
conn.close()

print(f"Loaded {len(crdb_ids)} musicbrainz_ids from CockroachDB")

# Iterate MongoDB docs and find missing IDs
missing_in_crdb = set()
cursor = track_metadata_collection.find({}, {"metadata.musicbrainz.recording_id": 1})

for doc in cursor:
    musicbrainz_id = doc.get("metadata", {}).get("musicbrainz", {}).get("recording_id")
    if musicbrainz_id:
        mid_str = str(musicbrainz_id).strip()
        if mid_str not in crdb_ids:
            missing_in_crdb.add(mid_str)

print(f"Found {len(missing_in_crdb)} MongoDB documents missing in CockroachDB")
print(missing_in_crdb)