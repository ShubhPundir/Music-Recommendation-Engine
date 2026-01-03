import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.mongodb import db
from database.cockroachdb import get_cockroach_connection


from collections import Counter


# MongoDB setup
track_metadata_collection = db['temp_tracks_metadata']

skipped_docs = []

cursor = track_metadata_collection.find({}, {"_id": 1, "metadata.musicbrainz.recording_id": 1})

print("Total MongoDB documents:", track_metadata_collection.count_documents({}))

for doc in cursor:
    try:
        musicbrainz = doc.get("metadata", {}).get("musicbrainz", {})
        musicbrainz_id = musicbrainz.get("recording_id") if isinstance(musicbrainz, dict) else None
        if not musicbrainz_id:
            skipped_docs.append((doc["_id"], musicbrainz))
    except Exception as e:
        skipped_docs.append((doc["_id"], f"Error: {str(e)}"))

print(f"\nTotal skipped documents: {len(skipped_docs)}")
for doc_id, issue in skipped_docs:
    print(f"Doc ID: {doc_id} | Issue: {issue}")

valid_ids = set()
cursor = track_metadata_collection.find({}, {"metadata.musicbrainz.recording_id": 1})

for doc in cursor:
    musicbrainz_id = (
        doc.get("metadata", {})
        .get("musicbrainz", {})
        .get("recording_id", None)
    )
    if musicbrainz_id is not None:
        valid_ids.add(str(musicbrainz_id).strip())

print(f"Documents with valid musicbrainz_id: {len(valid_ids)}")



# Find all musicbrainz_id values
all_ids = []
cursor = track_metadata_collection.find({}, {"metadata.musicbrainz.recording_id": 1})

for doc in cursor:
    musicbrainz_id = (
        doc.get("metadata", {})
        .get("musicbrainz", {})
        .get("recording_id", None)
    )
    if musicbrainz_id is not None:
        all_ids.append(str(musicbrainz_id).strip())

# Count occurrences of each musicbrainz_id
id_counts = Counter(all_ids)

# Filter for duplicates
duplicates = {key: value for key, value in id_counts.items() if value > 1}

print(f"Duplicate musicbrainz_id values (appeared more than once):")
for key, value in duplicates.items():
    print(f"{key}: {value} occurrences")


# Find duplicate musicbrainz_ids to delete (keeping only the first occurrence)
duplicate_ids = {key for key, value in duplicates.items() if value > 1}

for musicbrainz_id in duplicate_ids:
    # Find all documents with this musicbrainz_id
    cursor = track_metadata_collection.find({"metadata.musicbrainz.recording_id": musicbrainz_id})
    
    # Collect all document _id except for the first occurrence
    ids_to_delete = [doc["_id"] for idx, doc in enumerate(cursor) if idx > 0]
    
    # Delete the duplicates
    if ids_to_delete:
        delete_result = track_metadata_collection.delete_many({"_id": {"$in": ids_to_delete}})
        print(f"Deleted {delete_result.deleted_count} duplicates of {musicbrainz_id}")