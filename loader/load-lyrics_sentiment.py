import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv

# Import the necessary analysis functions
from sentiment_analysis.go_emotions import analyze_with_goEmotions
from sentiment_analysis.nrc_lexicon import analyze_emotions_nrc
from sentiment_analysis.text_blob import analyze_with_textblob
from sentiment_analysis.vader import analyze_with_vader

# === Unified CSV Saving Function ===
def save_analysis_to_csv(lyrics, lyric_id, csv_path="lyrics_analysis.csv"):
    
    # Perform analysis using all methods
    goemotions = analyze_with_goEmotions(lyrics)
    nrc = analyze_emotions_nrc(lyrics)
    textblob = analyze_with_textblob(lyrics)
    vader = analyze_with_vader(lyrics)
    
    # Extract GoEmotions results
    goemotion_results = {f"goemotion_{emotion['label']}": round(emotion['score'], 4) for emotion in goemotions}

    # Combine all results into a single row (structured dictionary)
    row = {
        "musicbrainz_id": lyric_id,
        **goemotion_results,
        **{f"nrc_{k}": v for k, v in nrc.items()},
        "textblob_polarity": textblob["TextBlob"]["Polarity"],  # Fixed key name
        "textblob_subjectivity": textblob["TextBlob"]["Subjectivity"],  # Fixed key name
        **{f"vader_{k}": v for k, v in vader.items()}
    }

    # Ensure the CSV file exists, then append the data
    file_exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()  # Write the header if the file is new
        writer.writerow(row)


# === Process Multiple Rows from Input CSV ===
def process_lyrics_from_csv(input_csv_path, output_csv_path="lyrics_analysis.csv"):
    # Read the input CSV and analyze each row
    with open(input_csv_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        count = 0
        for row in reader:
            # Extract the lyrics from 'genius_lyrics' or 'lastfm_wiki_content'
            text = row.get('genius_lyrics', "") or row.get('lastfm_wiki_content', "")
            musicbrainz_id = row.get('musicbrainz_id', "")
            
            save_analysis_to_csv(text, musicbrainz_id, output_csv_path)
            count += 1
            if(count % 25 == 0):
                print(f"{count} done")

# === Usage Example ===
# Provide the path to your input CSV
input_csv_path = 'loader/lyrics_202505062303.csv'
process_lyrics_from_csv(input_csv_path)