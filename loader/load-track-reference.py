import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.cockroachdb import get_cockroach_connection
from fetchDataApi.musicbrainz import get_track_details_musicbrainz

from concurrent.futures import ThreadPoolExecutor, as_completed
from psycopg2 import sql


def fetch_musicbrainz_ids():
    """
    Connects to CockroachDB and fetches all musicbrainz_ids from the lyrics table.
    """
    with get_cockroach_connection() as conn:
        musicbrainz_ids = []
        with conn.cursor() as cursor:
            query = sql.SQL("SELECT musicbrainz_id FROM lyrics WHERE musicbrainz_id IS NOT NULL")
            cursor.execute(query)
            results = cursor.fetchall()
            musicbrainz_ids = [row[0] for row in results]
    
    return musicbrainz_ids

def insert_track_details(track_data):
    """
    Inserts track details into the track_reference table in CockroachDB.
    """
    with get_cockroach_connection() as conn:
        with conn.cursor() as cursor:
            try:
                query = sql.SQL("""
                    INSERT INTO track_reference (
                        musicbrainz_id, title, artist, artist_id, album, album_id, 
                        release_date, country, length
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (musicbrainz_id) DO NOTHING;  -- To handle duplicates
                """)
                
                # Insert data into the track_reference table
                cursor.execute(query, (
                    track_data['recording_id'],  # musicbrainz_id
                    track_data['title'],
                    track_data['artist'],
                    track_data['artist_id'],
                    track_data['album'],
                    track_data['album_id'],
                    track_data['release_date'] if track_data['release_date'] else None,
                    track_data['country'],
                    track_data['length']  # Already in INT8 (milliseconds)
                ))
                conn.commit()
                print(f"Inserted track {track_data['recording_id']} into the database.")
            except Exception as e:
                print(f"Error inserting data for {track_data['recording_id']}: {str(e)}")

def process_musicbrainz_ids(musicbrainz_ids):
    """
    Fetches detailed track information from MusicBrainz for each musicbrainz_id
    and inserts it into CockroachDB.
    """

    
    with ThreadPoolExecutor(max_workers=1) as executor:  # Adjust max_workers based on your API rate limit.
        future_to_id = {executor.submit(get_track_details_musicbrainz, mbid): mbid for mbid in musicbrainz_ids}
        for future in as_completed(future_to_id):
            mbid = future_to_id[future]
            try:
                track_data = future.result()
                if 'error' not in track_data:
                    print(f"Successfully fetched data for {mbid}")
                    insert_track_details(track_data)
                else:
                    print(f"Error fetching data for {mbid}: {track_data['error']}")
            except Exception as e:
                print(f"        Error processing {mbid}: {str(e)}")
                cant.add(mbid)
                error += 1
def main():
    musicbrainz_ids = fetch_musicbrainz_ids()
    print(f"Found {len(musicbrainz_ids)} MusicBrainz IDs")
    error = 0
    cant = {}
    # Process all fetched IDs concurrently
    process_musicbrainz_ids(musicbrainz_ids)
    print("ERRORS: ", error)
    print(f'CANT: {cant}')
if __name__ == "__main__":
    main()