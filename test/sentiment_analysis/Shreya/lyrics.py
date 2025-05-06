import os
import json
from dotenv import load_dotenv
import lyricsgenius
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from collections import Counter

# 🧠 NLP Setup
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
vader = SentimentIntensityAnalyzer()

# Load GoEmotions BERT model
goemotions_model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_pipeline = pipeline("text-classification", model=goemotions_model, tokenizer=goemotions_tokenizer, return_all_scores=True)

# 🔐 Load Genius API Token
load_dotenv()
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_API_TOKEN")
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=15)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

# 📥 Fetch lyrics
def get_lyrics(song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)
        return song.lyrics if song else ""
    except Exception as e:
        return ""

# 🧠 Load NRC Emotion Lexicon
def load_nrc_lexicon(filepath="NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"):
    lexicon = {}
    with open(filepath, "r") as file:
        for line in file:
            word, emotion, association = line.strip().split('\t')
            if int(association) == 1:
                lexicon.setdefault(word, []).append(emotion)
    return lexicon

nrc_lexicon = load_nrc_lexicon()

# 🔍 NRC Emotion Analysis
def analyze_emotions_nrc(text, lexicon):
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in stop_words]
    emotions = []
    for word in words:
        if word in lexicon:
            emotions.extend(lexicon[word])
    return dict(Counter(emotions))

# 💬 Sentiment + Emotion Analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    vader_score = vader.polarity_scores(text)
    bert_scores = goemotions_pipeline(text[:512])[0]
    top_emotion = max(bert_scores, key=lambda x: x['score'])
    return {
        "TextBlob": {"Polarity": round(blob.polarity, 3), "Subjectivity": round(blob.subjectivity, 3)},
        "VADER": vader_score,
        "GoEmotions": {"Label": top_emotion["label"], "Score": round(top_emotion["score"], 3)}
    }

# ─── Lyrics Analysis Function ───────────────────────────────────────────────
def analyze_lyrics_full(song: str, artist: str):
    lyrics = get_lyrics(song, artist)
    if not lyrics:
        return {"song": song, "artist": artist, "error": "No lyrics found"}

    sentiment = analyze_sentiment(lyrics)
    nrc_emotions = analyze_emotions_nrc(lyrics, nrc_lexicon)

    result = {
        "song": song,
        "artist": artist,
        "lyrics": lyrics,
        "analysis": {
            "full_lyrics": {
                "sentiment": sentiment,
                "nrc_emotions": nrc_emotions
            }
        }
    }

    # Save JSON
    os.makedirs("results", exist_ok=True)
    filename = f"{artist.lower().replace(' ', '_')}_{song.lower().replace(' ', '_')}.json"
    filepath = os.path.join("results", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Analysis saved in '{filepath}'")
    return result

# ─── Runner ────────────────────────────────────────────────────────────────
def run():
    print("🎵 Enter Song Details")
    song = input("Song title: ").strip()
    artist = input("Artist name: ").strip()

    print(f"\n📥 Fetching lyrics and analyzing '{song}' by {artist}...\n")
    result = analyze_lyrics_full(song, artist)

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run()
