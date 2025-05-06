from dotenv import load_dotenv
import lyricsgenius
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import string

# 🧠 NLP Setup
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
vader = SentimentIntensityAnalyzer()
bert = pipeline("sentiment-analysis")

# 🔐 Load Genius API Token from .env file
load_dotenv()
GENIUS_ACCESS_TOKEN = "15TK9a5jJZpzxaxn39KcMjyrjr08ArZEllCdfYOe0E16mxjTs7x7BsmU-v7TLvBO"

if not GENIUS_ACCESS_TOKEN:
    print("❌ Genius API token not found. Please set GENIUS_API_TOKEN in your .env file.")
    exit(1)

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=15)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

# 🎵 Fetch lyrics
def get_lyrics(song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)
        return song.lyrics if song else ""
    except Exception as e:
        print(f"Error fetching lyrics: {e}")
        return ""

# 💬 Sentiment analysis using TextBlob, VADER, and BERT
def analyze_sentiment(text):
    result = {}
    blob = TextBlob(text)
    vader_score = vader.polarity_scores(text)
    bert_score = bert(text[:512])[0]  # BERT has 512-token input limit

    result["TextBlob"] = {
        "Polarity": round(blob.polarity, 3),
        "Subjectivity": round(blob.subjectivity, 3)
    }
    result["VADER"] = vader_score
    result["BERT"] = {
        "Label": bert_score["label"],
        "Score": round(bert_score["score"], 3)
    }
    return result

# 🔎 Run Analysis
def run():
    # print("🎵 Enter Song Details")
    song = "You really got a hold on me"
    artist = "The Beatles"

    print(f"\n📥 Fetching lyrics for '{song}' by {artist}...\n")
    lyrics = get_lyrics(song, artist)

    if not lyrics:
        print("❌ No lyrics found.")
        return

    print("✅ Lyrics fetched!")
    print("-" * 50)
    print("\nLyrics Preview:\n", "\n".join(lyrics.split("\n")[:10]), "\n...")

    print("\n🔍 Enter a word, sentence, or phrase to analyze:")
    query = input(">>> ").strip()

    print("\n📊 Sentiment Analysis Results:")
    sentiment = analyze_sentiment(query)
    for tool, scores in sentiment.items():
        print(f"\n🔹 {tool} Result:")
        for k, v in scores.items():
            print(f"   {k}: {v}")

    # Optional: analyze full lyrics
    analyze_full = input("\n⚙️ Do you want to analyze the *full lyrics* as well? (y/n): ")
    if analyze_full.lower().startswith("y"):
        full_sentiment = analyze_sentiment(lyrics)
        print("\n🎶 Full Lyrics Sentiment:")
        for tool, scores in full_sentiment.items():
            print(f"\n🔹 {tool} Result:")
            for k, v in scores.items():
                print(f"   {k}: {v}")

if __name__ == "__main__":
    run()
