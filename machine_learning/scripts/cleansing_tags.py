from database.cockroachdb import get_cockroach_connection
import json

def get_remove_keywords():
    """Returns list of keywords to remove from tags"""
    return [
        # Artist names / people
        '50 cent','andre 3000','aphex twin','ariana grande','ashley gorley','benny blanco','billie eilish','billy joel',
        'bruno mars','chance the rapper','chris stapleton','david guetta','demi lovato','dr dre','drake','ed sheeran',
        'finneas','frank ocean','jackson mahomes','jason derulo','justin bieber','kacey musgraves','kanye west','kehlani',
        'kendrick lamar','lady gaga','lana del rey','luke bryan','maroon 5','madison beer','miley cyrus','missy elliott',
        'mos def','nas','one direction','pharrell williams','rihanna','quavo','queen','sza','talib kweli','tame impala',
        'taylor swift','tchaikovsky','the beatles','the kid laroi','the weeknd','timbaland','travis scott','violeta parra',
        'willie nelson',
        # Inappropriate / non-genre
        'adolf','hitler','climate terrorist','kkk','pussy','weed','white music',
        # Years / decades / numbers
        '00s','10s','2 of 10 stars','2004','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019',
        '2020','2021','2022','2023','2024','50 cent','60s','70s','80s','90s',
        # Subjective / filler
        'aoty','amazing','awesome','best','better','calm','catchy','cool','dictionary','fun','funny','good','great','hot',
        'i ','im ','my','oh ','perfect','piggy bank','playboi carti','reference','relatable','sad','slay','sober','solo',
        'songs','test','this','truth','unbroken','underrated','unique','witty','worst'
    ]

def get_genre_mapping():
    """Returns dictionary mapping normalized genres to their variants"""
    return {
        'hip_hop-rap': ['hip-hop', 'hiphop', 'hip hop', 'gangsta', 'southern hip hop', 'rap', 'trap', 'trap beat', 'memphis rap', 'pop rap'],
        'pop': ['pop', 'teen pop', 'pop alternative', 'pop punk', 'electropop', 'synth-pop', 'hyperpop', 'indie pop', 'bedroom pop', 'soft pop', 'art pop', 'baroque pop', 'chamber pop', 'dark pop', 'dance-pop'],
        'rock-metal-psychedelic': ['rock', 'alternative rock', 'indie rock', 'classic rock', 'hard rock', 'soft rock', 'punk', 'blues rock', 'garage rock', 'glam rock', 'post-rock', 'roots rock', 'rock n roll', 'rockabilly', 'k-rock', 'synthrock', 'psychedelic', 'psychedelic rock', 'psychedelic folk', 'psychedelic pop', 'psychedelic soul', 'metal', 'death', 'black', 'hardcore'],
        'blues-r&b-soul': ['blues', 'blues-rock', 'country blues', 'rnb', 'neo-soul', 'neo soul', 'rhythm and blues', 'soul'],
        'folk-classical-country-jazz': ['folk', 'indie folk', 'folk rock', 'folk pop', 'chamber folk', 'psychedelic folk', 'americana', 'american folk', 'country', 'contemporary country', 'bro-country', 'alt-country', 'country pop', 'country rock', 'country soul', 'cuntry', 'classical', 'classical music', 'modern classical', 'western classical', 'italian opera', 'symphony', 'klassik', 'jazz', 'jazz rap', 'jazz rock', 'smooth jazz', 'nu-jazz'],
        'electronic-funk-disco-dance': ['electronic', 'edm', 'electro', 'electroclash', 'electrorock', 'progressive electronic', 'synthwave', 'futurepop', 'nu-disco', 'euro house', 'tribal house', 'tropical house', 'house', 'deep house', 'disco', 'dance', 'dance-pop', 'downtempo', 'trip hop', 'trip-hop', 'chillwave', 'hyperpop', 'funk', 'g-funk', 'funk rock', 'funktronica', 'brazilian funk', 'bounce', 'baile funk', 'synth funk'],
        'opera-musical-theater-soundtrack-vocal-a_cappella': ['soundtrack', 'soundtracks', 'opera', 'traditional pop', 'orchestral', 'a cappella', 'acapella', 'vocal', 'vocals', 'vocal harmonies', 'ambient', 'chill', 'downtempo', 'dream pop', 'hypnagogic pop', 'cinematic', 'space age pop'],
        # Add more genre mappings as needed...
    }

def cleanse_tags():
    """Main function to cleanse LastFM tags in the database"""
    
    # Connect to database
    conn = get_cockroach_connection()
    cursor = conn.cursor()

    # Run DDL in autocommit to avoid aborting a long-running transaction on error
    _prev_autocommit = conn.autocommit
    conn.autocommit = True
    try:
        cursor.execute("""
            ALTER TABLE tracks_metadata
            ADD COLUMN IF NOT EXISTS final_tags JSONB
        """)
        try:
            cursor.execute("""
                ALTER TABLE tracks_metadata
                ALTER COLUMN final_tags TYPE JSONB USING 
                    CASE 
                        WHEN final_tags IS NULL THEN NULL 
                        WHEN left(trim(both ' ' from final_tags::STRING), 1) = '[' THEN final_tags::JSONB
                        ELSE (
                            to_json(
                                string_to_array(
                                    replace(replace(trim(both '[]' from final_tags::STRING), '"', ''), '\\'', ''), ','
                                )
                            )::JSONB
                        )
                    END
            """)
        except Exception:
            # Type already correct or conversion not needed
            pass
    finally:
        conn.autocommit = _prev_autocommit
    
    # Fetch all tracks with their tags
    cursor.execute("""
        SELECT mongo_id, lastfm_tags 
        FROM tracks_metadata 
        WHERE lastfm_tags IS NOT NULL
    """)
    
    records = cursor.fetchall()
    print(f"Processing {len(records)} tracks with tags...")

    # Get filtering configs
    remove_keywords = get_remove_keywords()
    genre_mapping = get_genre_mapping()
    
    # Process each record
    for mongo_id, tags in records:
        if not tags:
            continue
            
        # Parse tags to a Python list, favoring JSON arrays
        if isinstance(tags, list):
            original_tags = [t for t in tags if isinstance(t, str)]
        else:
            text_value = str(tags).strip()
            parsed = None
            if text_value.startswith('[') and text_value.endswith(']'):
                try:
                    parsed = json.loads(text_value)
                except Exception:
                    parsed = None
            if isinstance(parsed, list):
                original_tags = [t for t in parsed if isinstance(t, str)]
            else:
                # Fallback: split by comma, stripping quotes and brackets
                text_value = text_value.strip('[]')
                parts = [p.strip().strip('"').strip("'") for p in text_value.split(',') if p.strip()]
                original_tags = parts
        
        # Remove unwanted tags
        cleaned_tags = []
        for tag in original_tags:
            tag_stripped = tag.strip()
            if not tag_stripped:
                continue
            if any(keyword in tag_stripped.lower() for keyword in remove_keywords):
                continue
            cleaned_tags.append(tag_stripped)
        
        # Normalize genres using mapping; ignore unmapped here
        normalized_tags = []
        for tag in cleaned_tags:
            tag_lower = tag.lower()
            normalized = False
            for main_genre, variants in genre_mapping.items():
                if any(variant.lower() in tag_lower for variant in variants):
                    normalized_tags.append(main_genre)
                    normalized = True
                    break
            # do not append anything for unmapped tags at this stage
                
        # Remove duplicates while preserving order (case-insensitive uniqueness)
        seen_lower = set()
        final_list = []
        for item in normalized_tags:
            key = item.lower()
            if key in seen_lower:
                continue
            seen_lower.add(key)
            final_list.append(item)
        
        # If nothing matched, fallback to single 'others'
        if not final_list:
            final_list = ['others']

        # Update database
        cursor.execute("""
            UPDATE tracks_metadata 
            SET final_tags = %s::JSONB 
            WHERE mongo_id = %s
        """, (json.dumps(final_list), mongo_id))
    
    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Tag cleansing completed successfully!")

if __name__ == "__main__":
    cleanse_tags()