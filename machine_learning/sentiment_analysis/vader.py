from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()

def analyze_with_vader(text) -> dict:
    vader_score = vader.polarity_scores(text)
    
    return vader_score


# lyrics = '''"94 Contributors\nTranslations\nPolski\nEspañol\nРусский\nRomână\nPortuguês\nItaliano\nHebrew\nDeutsch\nFrançais\nNederlands\nDansk\nraindrops (an angel cried) Lyrics\nThe a capella “raindrops (an angel cried)” is the introduction to Ariana Grande’s fourth studio album, Sweetener. This song is a cover of The Four Seasons' “An Angel Cried.”\n\nThe song was first teased in her… \nRead More\n\xa0\n[Verse]\nWhen raindrops fell down from the sky\nThe day you left me, an angel cried\nOh, she cried\nAn angel cried, she cried"'''

# print(analyze_with_vader(lyrics))