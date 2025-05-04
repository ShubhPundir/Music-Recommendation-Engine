import os
import re
import json
import psycopg2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models import Word2Vec
from collections import Counter
from dotenv import load_dotenv

# ─── NLP Setup ─────────────────────────────────────────────────────
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
vader = SentimentIntensityAnalyzer()

# ─── Load GoEmotions Model ─────────────────────────────────────────
print("🔁 Loading GoEmotions model...")
goemotions_model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_pipeline = pipeline("text-classification", model=goemotions_model, tokenizer=goemotions_tokenizer, top_k=None, device=-1)

# ─── Load Environment Variables ────────────────────────────────────
load_dotenv()
COCKROACH_USER = os.getenv("COCKROACH_USER")
COCKROACH_PASS = os.getenv("COCKROACH_PASS")
COCKROACH_HOST = os.getenv("COCKROACH_HOST")
COCKROACH_PORT = os.getenv("COCKROACH_PORT")

# ─── Fetch Full Record from CockroachDB ─────────────────────────────
def fetch_record_from_cockroach(musicbrainz_id: str):
    try:
        conn = psycopg2.connect(
            dbname="music",
            user=COCKROACH_USER,
            password=COCKROACH_PASS,
            host=COCKROACH_HOST,
            port=COCKROACH_PORT,
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute(
            """
            SELECT musicbrainz_id, genius_lyrics, genius_url
            FROM lyrics
            WHERE musicbrainz_id = %s
            LIMIT 1;
            """,
            (musicbrainz_id,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            mbid, lyrics, url = row
            return {
                "musicbrainz_id": str(mbid),
                "genius_lyrics": lyrics,
                "genius_url": url
            }
    except Exception as e:
        print(f"❌ CockroachDB error: {e}")
    return {}

# ─── NRC Emotion Lexicon ───────────────────────────────────────────
def load_nrc_lexicon(filepath="NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"):
    lexicon = {}
    with open(filepath, "r") as file:
        for line in file:
            word, emotion, assoc = line.strip().split('\t')
            if assoc == '1':
                lexicon.setdefault(word, []).append(emotion)
    return lexicon

nrc_lexicon = load_nrc_lexicon()

def analyze_emotions_nrc(text: str):
    toks = [w for w in word_tokenize(text.lower()) if w.isalpha() and w not in stop_words]
    ctr = Counter()
    for w in toks:
        for emo in nrc_lexicon.get(w, []):
            ctr[emo] += 1
    return dict(ctr)

# ─── Sentiment & Topic Modeling ────────────────────────────────────
def analyze_sentiment(text: str):
    blob = TextBlob(text)
    vd = vader.polarity_scores(text)
    bert_scores = goemotions_pipeline(text[:512])[0]
    top = max(bert_scores, key=lambda x: x['score'])
    return {
        "TextBlob": {"polarity": round(blob.polarity,3), "subjectivity": round(blob.subjectivity,3)},
        "VADER": vd,
        "GoEmotions": {"label": top['label'], "score": round(top['score'],3)}
    }

def lda_topics(text: str, num_topics=3, num_words=5, chunk_size=50, step=25):
    """
    Improved LDA topic extraction by creating pseudo-documents from overlapping chunks of the lyrics.
    """
    tokens = [w for w in word_tokenize(text.lower()) if w.isalpha() and w not in stop_words]
    if len(tokens) < chunk_size:
        return [{"topic": 0, "keywords": tokens[:num_words]}]  # fallback

    # Create overlapping chunks
    chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens) - chunk_size + 1, step)]
    
    # Build dictionary and corpus
    dct = corpora.Dictionary(chunks)
    corpus = [dct.doc2bow(chunk) for chunk in chunks]

    # Train LDA model
    lda = LdaModel(corpus=corpus, id2word=dct, num_topics=num_topics, passes=10, random_state=42)

    # Extract topics
    topics = []
    for i in range(num_topics):
        topic_keywords = [word for word, _ in lda.show_topic(i, topn=num_words)]
        topics.append({"topic": i, "keywords": topic_keywords})
    
    return topics


# ─── Word2Vec Embedding ───────────────────────────────────────────
def vectorize_text(text: str):
    toks = [w for w in word_tokenize(text.lower()) if w.isalpha() and w not in stop_words]
    if not toks:
        return []
    model = Word2Vec([toks], vector_size=200, window=5, min_count=1, workers=2, sg=1)
    vec = sum(model.wv[w] for w in toks if w in model.wv) / len(toks)
    return vec.tolist()

# ─── Main Analysis ─────────────────────────────────────────────────
def analyze_lyrics_full(musicbrainz_id: str):
    rec = fetch_record_from_cockroach(musicbrainz_id)
    if not rec:
        return {"musicbrainz_id": musicbrainz_id, "error": "No record found"}

    lyrics = rec.get("genius_lyrics", "")
    if not lyrics:
        return {"musicbrainz_id": musicbrainz_id, "error": "No lyrics in record"}

    sentiment = analyze_sentiment(lyrics)
    nrc_emotions = analyze_emotions_nrc(lyrics)
    topics = lda_topics(lyrics)
    vector = vectorize_text(lyrics)

    result = {
        "musicbrainz_id": musicbrainz_id,
        **rec,
        "analysis": {
            "sentiment": sentiment,
            "nrc_emotions": nrc_emotions,
            "topics": topics,
            "word2vec_vector": vector
        }
    }

    os.makedirs("results", exist_ok=True)
    fn = f"{musicbrainz_id}.json"
    with open(os.path.join("results", fn), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Analysis saved to results/{fn}")
    return result

# ─── CLI ─────────────────────────────────────────────────────────
def run():
    print("🎵 1) Analyze by MusicBrainz ID  2) Test on Sample")
    c = input("Choice: ").strip()
    if c == "1":
        mbid = input("Enter MusicBrainz ID: ").strip()
        print(f"\nAnalyzing song with MusicBrainz ID: {mbid}...\n")
        res = analyze_lyrics_full(mbid)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        txt = input("Sample text: ").strip()
        print(json.dumps(analyze_sentiment(txt), indent=2))
        print(json.dumps(analyze_emotions_nrc(txt), indent=2))
        print(json.dumps(lda_topics(txt), indent=2))
        print(vectorize_text(txt))

if __name__ == "__main__":
    run()
