from textblob import TextBlob
from pprint import pprint

def analyze_with_textblob(text):
    blob = TextBlob(text)
    result = {}
    result["TextBlob"] = {
        "Polarity": round(blob.polarity, 3),
        "Subjectivity": round(blob.subjectivity, 3)
    }
    return result

# lyrics = '''"94 Contributors\nTranslations\nPolski\nEspañol\nРусский\nRomână\nPortuguês\nItaliano\nHebrew\nDeutsch\nFrançais\nNederlands\nDansk\nraindrops (an angel cried) Lyrics\nThe a capella “raindrops (an angel cried)” is the introduction to Ariana Grande’s fourth studio album, Sweetener. This song is a cover of The Four Seasons' “An Angel Cried.”\n\nThe song was first teased in her… \nRead More\n\xa0\n[Verse]\nWhen raindrops fell down from the sky\nThe day you left me, an angel cried\nOh, she cried\nAn angel cried, she cried"'''

# pprint(analyze_with_textblob(lyrics))