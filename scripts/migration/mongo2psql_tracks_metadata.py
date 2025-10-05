import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import json
from typing import Dict, Any, List
from psycopg2.extras import execute_batch
from psycopg2.extensions import connection as PGConnection
from bson import ObjectId

from database.cockroachdb import get_cockroach_connection
from database.mongodb import db


MONGO_COLLECTION = db["tracks_metadata"]

def transform(doc: dict) -> dict:
    """Transform MongoDB track document into Postgres-ready dict with flattened metadata."""
    # Convert ObjectId
    if isinstance(doc["_id"], ObjectId):
        mongo_id = str(doc["_id"])
    elif isinstance(doc["_id"], dict) and "$oid" in doc["_id"]:
        mongo_id = doc["_id"]["$oid"]
    else:
        mongo_id = str(doc["_id"])

    metadata = doc.get("metadata", {}) or {}

    musicbrainz = metadata.get("musicbrainz", {}) or {}
    lastfm = metadata.get("lastfm", {}) or {}
    genius = metadata.get("genius", {}) or {}

    return {
        "mongo_id": mongo_id,
        "artist": doc.get("artist"),
        "track": doc.get("track"),
        "album": doc.get("album"),

        # MusicBrainz
        "musicbrainz_recording_id": musicbrainz.get("recording_id"),
        "musicbrainz_title": musicbrainz.get("title"),
        "musicbrainz_artist": musicbrainz.get("artist"),
        "musicbrainz_artist_id": musicbrainz.get("artist_id"),
        "musicbrainz_album": musicbrainz.get("album"),
        "musicbrainz_album_id": musicbrainz.get("album_id"),
        "musicbrainz_release_date": musicbrainz.get("release_date"),
        "musicbrainz_country": musicbrainz.get("country"),
        "musicbrainz_length": musicbrainz.get("length"),

        # LastFM
        "lastfm_tags": json.dumps(lastfm.get("tags", [])),
        "lastfm_similar_tracks": json.dumps(lastfm.get("similar_tracks", [])),

        # Genius
        "genius_title": genius.get("title"),
        "genius_artist": genius.get("artist"),
        "genius_album": genius.get("album"),
        "genius_release_date": genius.get("release_date"),
        "genius_song_art_image_url": genius.get("song_art_image_url"),
        "genius_verified": genius.get("verified"),
    }


INSERT_QUERY = """
INSERT INTO tracks_metadata (
    mongo_id, artist, track, album,
    musicbrainz_recording_id, musicbrainz_title, musicbrainz_artist, musicbrainz_artist_id,
    musicbrainz_album, musicbrainz_album_id, musicbrainz_release_date, musicbrainz_country, musicbrainz_length,
    lastfm_tags, lastfm_similar_tracks,
    genius_title, genius_artist, genius_album, genius_release_date, genius_song_art_image_url, genius_verified
) VALUES (
    %(mongo_id)s, %(artist)s, %(track)s, %(album)s,
    %(musicbrainz_recording_id)s, %(musicbrainz_title)s, %(musicbrainz_artist)s, %(musicbrainz_artist_id)s,
    %(musicbrainz_album)s, %(musicbrainz_album_id)s, %(musicbrainz_release_date)s, %(musicbrainz_country)s, %(musicbrainz_length)s,
    %(lastfm_tags)s::jsonb, %(lastfm_similar_tracks)s::jsonb,
    %(genius_title)s, %(genius_artist)s, %(genius_album)s, %(genius_release_date)s, %(genius_song_art_image_url)s, %(genius_verified)s
)
ON CONFLICT (mongo_id) DO NOTHING;
"""

def fetch_docs() -> List[Dict[str, Any]]:
    print("Fetching docs from MongoDB...")
    docs = list(MONGO_COLLECTION.find())
    print("Found %d records.", len(docs))
    return docs

def insert_records(records: List[Dict[str, Any]], conn: PGConnection) -> None:
    print("Inserting %d records into CockroachDB...", len(records))
    with conn.cursor() as cur:
        execute_batch(cur, INSERT_QUERY, records, page_size=100)
    conn.commit()
    print("✅ Migration complete: %d records inserted.", len(records))

def migrate() -> None:
    docs = fetch_docs()
    records = [transform(doc) for doc in docs]

    with get_cockroach_connection() as conn:
        insert_records(records, conn)

if __name__ == "__main__":
    migrate()
