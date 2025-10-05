import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import json
from typing import Dict, Any, List
from psycopg2.extras import execute_batch
from psycopg2.extensions import connection as PGConnection
from bson import ObjectId

from database.cockroachdb import get_cockroach_connection
from database.mongodb import db

# --- Logging ---
 # ...existing code...

# --- Mongo Client ---
MONGO_COLLECTION = db["artists"]

# --- Transformation ---
def transform(doc: dict) -> dict:
    """Transform MongoDB artist document into Postgres-ready dict with flattened wiki."""
    # Convert Mongo ObjectId → string
    if isinstance(doc["_id"], ObjectId):
        mongo_id = str(doc["_id"])
    elif isinstance(doc["_id"], dict) and "$oid" in doc["_id"]:
        mongo_id = doc["_id"]["$oid"]
    else:
        mongo_id = str(doc["_id"])

    wiki = doc.get("wiki", {}) or {}

    return {
        "mongo_id": mongo_id,
        "name": doc.get("name"),
        "tags": json.dumps(doc.get("tags", [])),  # JSONB
        "similar_artists": json.dumps(doc.get("similar_artists", [])),  # JSONB
        "wiki_published": wiki.get("published"),
        "wiki_summary": wiki.get("summary"),
        "wiki_content": wiki.get("content"),
        "musicbrainz_id": doc.get("musicbrainz_id"),
    }

# --- Insert Query ---
INSERT_QUERY = """
INSERT INTO artists (
    mongo_id, name, tags, similar_artists,
    wiki_published, wiki_summary, wiki_content, musicbrainz_id
) VALUES (
    %(mongo_id)s, %(name)s, %(tags)s::jsonb, %(similar_artists)s::jsonb,
    %(wiki_published)s, %(wiki_summary)s, %(wiki_content)s, %(musicbrainz_id)s
)
ON CONFLICT (mongo_id) DO NOTHING;
"""

# --- Migration helpers ---
def fetch_docs() -> List[Dict[str, Any]]:
    """Fetch all documents from MongoDB."""
    print("Fetching docs from MongoDB...")
    docs = list(MONGO_COLLECTION.find())
    print(f"Found {len(docs)} records.")
    return docs


def insert_records(records: List[Dict[str, Any]], conn: PGConnection) -> None:
    """Insert transformed records into CockroachDB/Postgres."""
    print(f"Inserting {len(records)} records into CockroachDB...")
    with conn.cursor() as cur:
        execute_batch(cur, INSERT_QUERY, records, page_size=100)
    conn.commit()
    print(f"✅ Migration complete: {len(records)} records inserted.")


def migrate() -> None:
    """Main migration workflow."""
    docs = fetch_docs()
    records = [transform(doc) for doc in docs]

    with get_cockroach_connection() as conn:
        insert_records(records, conn)


if __name__ == "__main__":
    migrate()
