import os
from dotenv import load_dotenv
import lyricsgenius
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from collections import Counter
import torch

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

if not GENIUS_ACCESS_TOKEN:
    print("❌ Genius API token not found. Please set GENIUS_API_TOKEN in your .env file.")
    exit(1)

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=15)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

# 📥 Fetch lyrics
def get_lyrics(song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)
        return song.lyrics if song else ""
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
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
    result = {}
    blob = TextBlob(text)
    vader_score = vader.polarity_scores(text)

    bert_scores = goemotions_pipeline(text[:512])[0]
    top_emotion = max(bert_scores, key=lambda x: x['score'])

    result["TextBlob"] = {
        "Polarity": round(blob.polarity, 3),
        "Subjectivity": round(blob.subjectivity, 3)
    }
    result["VADER"] = vader_score
    result["GoEmotions"] = {
        "Label": top_emotion["label"],
        "Score": round(top_emotion["score"], 3)
    }
    return result

def run():
    print("🎵 Enter Song Details")
    song = input("Song title: ")
    artist = input("Artist name: ")

    print(f"\n📥 Fetching lyrics for '{song}' by {artist}...\n")
    lyrics = get_lyrics(song, artist)

    if not lyrics:
        print("❌ No lyrics found.")
        return

    print("✅ Lyrics fetched!")
    print("-" * 50)

    # Option A: Always show full lyrics
    # print("\n🎤 Full Lyrics:\n")
    # print(lyrics)
    # print("\n" + "-" * 50)

    # Option B: Ask user whether to show full lyrics
    show_all = input("👀 View full lyrics? (y/n): ")
    if show_all.lower().startswith("y"):
        print("\n🎤 Full Lyrics:\n")
        print(lyrics)
    else:
        print("\nLyrics Preview:\n", "\n".join(lyrics.split("\n")[:10]), "\n...")

    print("\n🔍 Enter a word, sentence, or phrase to analyze:")
    query = input(">>> ").strip()

    print("\n📊 Sentiment Analysis Results:")
    sentiment = analyze_sentiment(query)
    for tool, scores in sentiment.items():
        print(f"\n🔹 {tool} Result:")
        for k, v in scores.items():
            print(f"   {k}: {v}")

    analyze_full = input("\n⚙️ Do you want to analyze the *full lyrics* as well? (y/n): ")
    if analyze_full.lower().startswith("y"):
        full_sentiment = analyze_sentiment(lyrics)
        print("\n🎶 Full Lyrics Sentiment:")
        for tool, scores in full_sentiment.items():
            print(f"\n🔹 {tool} Result:")
            for k, v in scores.items():
                print(f"   {k}: {v}")

        full_emotions = analyze_emotions_nrc(lyrics, nrc_lexicon)
        print("\n🧠 Emotion Analysis for Full Lyrics using NRC Lexicon:")
        for emotion, count in sorted(full_emotions.items(), key=lambda x: -x[1]):
            print(f"   {emotion}: {count}")

if __name__ == "__main__":
    run()
