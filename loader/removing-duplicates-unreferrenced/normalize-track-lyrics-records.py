import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongodb import db
from database.cockroachdb import get_cockroach_connection

# MongoDB setup
track_metadata_collection = db['temp_tracks_metadata']

# Fetch MongoDB IDs
mongo_ids = set()
mongo_docs_to_delete = []
for doc in track_metadata_collection.find({}, {"_id": 1, "metadata.musicbrainz.recording_id": 1}):
    musicbrainz_id = doc.get("metadata", {}).get("musicbrainz", {}).get('recording_id')
    if musicbrainz_id:
        mongo_ids.add(musicbrainz_id)
    else:
        mongo_docs_to_delete.append(doc["_id"])  # Also track any malformed entries with no ID

print(f"Mongo IDs with musicbrainz_id: {len(mongo_ids)}")

# Fetch CockroachDB IDs
conn = get_cockroach_connection()
crdb_ids = set()
with conn.cursor() as cursor:
    cursor.execute("SELECT musicbrainz_id FROM lyrics_temp;")
    crdb_ids.update(row[0] for row in cursor.fetchall())
conn.close()

print(f"Cockroach IDs with musicbrainz_id: {len(crdb_ids)}")

# Find extras
extra_in_mongo = mongo_ids - crdb_ids
extra_in_crdb = crdb_ids - mongo_ids

print(f"IDs in MongoDB but not in CockroachDB: {len(extra_in_mongo)}")
print(f"IDs in CockroachDB but not in MongoDB: {len(extra_in_crdb)}")

print(len(mongo_docs_to_delete), f': {mongo_docs_to_delete}')

# DELETE from MongoDB
if extra_in_mongo or mongo_docs_to_delete:
    delete_filter = {
        "$or": [
            {"metadata.musicbrainz.recording_id": {"$in": list(extra_in_mongo)}}
        ] + ([{"_id": {"$in": mongo_docs_to_delete}}] if mongo_docs_to_delete else [])
    }
    result = track_metadata_collection.delete_many(delete_filter)
    print(f"Deleted {result.deleted_count} documents from MongoDB.")

    
delete_result = track_metadata_collection.delete_many({
    "metadata.musicbrainz.recording_id": {"$in": list(extra_in_mongo)}
})

print(f"Deleted {delete_result.deleted_count} unmatched valid documents from MongoDB.")


# DELETE from CockroachDB
if extra_in_crdb:
    conn = get_cockroach_connection()
    with conn.cursor() as cursor:
        # Use batching to avoid SQL issues
        batch_size = 100
        to_delete = list(extra_in_crdb)
        for i in range(0, len(to_delete), batch_size):
            batch = to_delete[i:i+batch_size]
            sql = "DELETE FROM lyrics_temp WHERE musicbrainz_id = ANY(%s);"
            cursor.execute(sql, (batch,))
    conn.commit()
    conn.close()
    print(f"Deleted {len(extra_in_crdb)} rows from CockroachDB.")



# OUTPUT:

# Pinged your deployment. You successfully connected to MongoDB!
# Mongo IDs with musicbrainz_id: 1096
# Cockroach IDs with musicbrainz_id: 1114
# IDs in MongoDB but not in CockroachDB: 0
# IDs in CockroachDB but not in MongoDB: 18
# 30
# Deleted 30 documents from MongoDB.
# Deleted 18 rows from CockroachDB.