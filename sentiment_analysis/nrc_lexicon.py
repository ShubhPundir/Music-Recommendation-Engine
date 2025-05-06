from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from pprint import pprint

# Setup
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# All 10 NRC emotion categories
NRC_EMOTIONS = [
    'anger', 'anticipation', 'disgust', 'fear', 'joy',
    'negative', 'positive', 'sadness', 'surprise', 'trust'
]

# Load NRC Emotion Lexicon
def load_nrc_lexicon(filepath="sentiment_analysis\\NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"):
    lexicon = {}
    with open(filepath, "r") as file:
        for line in file:
            word, emotion, association = line.strip().split('\t')
            if int(association) == 1:
                lexicon.setdefault(word, []).append(emotion)
    return lexicon

nrc_lexicon = load_nrc_lexicon()

# Emotion Analysis with Consistent Output
def analyze_emotions_nrc(text, lexicon=nrc_lexicon):
    if not text:
        return {f"{emotion}": 0 for emotion in NRC_EMOTIONS}

    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in stop_words]

    emotions = []
    for word in words:
        if word in lexicon:
            emotions.extend(lexicon[word])

    emotion_counts = Counter(emotions)

    # Ensure all keys are returned
    return {f"{emotion}": emotion_counts.get(emotion, 0) for emotion in NRC_EMOTIONS}



# lyrics = '''"94 Contributors\nTranslations\nPolski\nEspañol\nРусский\nRomână\nPortuguês\nItaliano\nHebrew\nDeutsch\nFrançais\nNederlands\nDansk\nraindrops (an angel cried) Lyrics\nThe a capella “raindrops (an angel cried)” is the introduction to Ariana Grande’s fourth studio album, Sweetener. This song is a cover of The Four Seasons' “An Angel Cried.”\n\nThe song was first teased in her… \nRead More\n\xa0\n[Verse]\nWhen raindrops fell down from the sky\nThe day you left me, an angel cried\nOh, she cried\nAn angel cried, she cried"'''

# x = analyze_emotions_nrc("joyful and surprising events bring happiness")
# pprint(x)