import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import json
from datetime import datetime
from psycopg2.extras import execute_batch
from psycopg2.extensions import connection as PGConnection
from database.cockroachdb import get_cockroach_connection
from database.mongodb import db
from typing import Optional, Dict, Any, List
from bson import ObjectId
import logging

# --- Mongo Client ---
MONGO_COLLECTION = db["albums"]

# --- Transformation ---
def parse_date(date_str: Optional[str]) -> Optional[datetime.date]:
    """Safely parse a YYYY-MM-DD string into a date object."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        logging.warning("Invalid date format: %s", date_str)
        return None


def transform(doc: dict) -> dict:
    # Convert Mongo ObjectId → string
    if isinstance(doc["_id"], ObjectId):
        mongo_id = str(doc["_id"])
    elif isinstance(doc["_id"], dict) and "$oid" in doc["_id"]:
        mongo_id = doc["_id"]["$oid"]
    else:
        mongo_id = str(doc["_id"])

    return {
        "mongo_id": mongo_id,
        "name": doc.get("name"),
        "artist": doc.get("artist"),
        "url": doc.get("url"),
        "playcount": int(doc.get("playcount", 0)) if doc.get("playcount") else None,
        "listeners": int(doc.get("listeners", 0)) if doc.get("listeners") else None,
        "tags": json.dumps(doc.get("tags", [])),         # JSONB
        "tracks": json.dumps(doc.get("tracks", [])),     # JSONB
        "images": json.dumps(doc.get("images", {})),     # JSONB
        "wiki_summary": doc.get("wiki_summary"),
    }
# --- Insert Query ---
INSERT_QUERY = """
INSERT INTO albums (
    mongo_id, name, artist, url,
    playcount, listeners,
    tags, tracks, images, wiki_summary
) VALUES (
    %(mongo_id)s, %(name)s, %(artist)s, %(url)s,
    %(playcount)s, %(listeners)s,
    %(tags)s::jsonb, %(tracks)s::jsonb, %(images)s::jsonb, %(wiki_summary)s
)
ON CONFLICT (mongo_id) DO NOTHING;
"""

# --- Migration ---
def fetch_docs() -> List[Dict[str, Any]]:
    """Fetch all documents from MongoDB."""
    print("Fetching docs from Mongo...")
    docs = list(MONGO_COLLECTION.find())
    print("Found %d records.", len(docs))
    return docs


# --- Main Migration ---
def migrate():
    print("Fetching docs from Mongo...")
    docs = list(MONGO_COLLECTION.find())
    print(f"Found {len(docs)} records.")

    records = [transform(doc) for doc in docs]

    print("Inserting into CockroachDB...")
    conn = get_cockroach_connection()
    cur = conn.cursor()
    execute_batch(cur, INSERT_QUERY, records, page_size=100)
    conn.commit()
    cur.close()
    conn.close()

    print(f"✅ Migration complete: {len(records)} records inserted.")

def insert_records(records: List[Dict[str, Any]], conn: PGConnection) -> None:
    """Insert transformed records into CockroachDB/Postgres."""
    logging.info("Inserting %d records into CockroachDB...", len(records))
    with conn.cursor() as cur:
        execute_batch(cur, INSERT_QUERY, records, page_size=100)
    conn.commit()
    logging.info("✅ Migration complete: %d records inserted.", len(records))


def migrate() -> None:
    """Main migration workflow."""
    docs = fetch_docs()
    records = [transform(doc) for doc in docs]

    with get_cockroach_connection() as conn:
        insert_records(records, conn)


if __name__ == "__main__":
    migrate()