DROP TABLE IF EXISTS lyrics_sentiments;
CREATE TABLE lyrics_sentiments (
    musicbrainz_id UUID PRIMARY KEY, -- Unique identifier for the track, also serves as primary key
    goemotion_sadness REAL,
    goemotion_realization REAL,
    goemotion_neutral REAL,
    goemotion_love REAL,
    goemotion_grief REAL,
    goemotion_amusement REAL,
    goemotion_gratitude REAL,
    goemotion_disappointment REAL,
    goemotion_surprise REAL,
    goemotion_nervousness REAL,
    goemotion_embarrassment REAL,
    goemotion_remorse REAL,
    goemotion_joy REAL,
    goemotion_fear REAL,
    goemotion_excitement REAL,
    goemotion_anger REAL,
    goemotion_pride REAL,
    goemotion_caring REAL,
    goemotion_disgust REAL,
    goemotion_confusion REAL,
    goemotion_optimism REAL,
    goemotion_relief REAL,
    goemotion_desire REAL,
    goemotion_annoyance REAL,
    goemotion_approval REAL,
    goemotion_admiration REAL,
    goemotion_disapproval REAL,
    goemotion_curiosity REAL,
    nrc_anger REAL, -- Changed from INTEGER to REAL
    nrc_anticipation REAL, -- Changed from INTEGER to REAL
    nrc_disgust REAL, -- Changed from INTEGER to REAL
    nrc_fear REAL, -- Changed from INTEGER to REAL
    nrc_joy REAL, -- Changed from INTEGER to REAL
    nrc_negative REAL, -- Changed from INTEGER to REAL
    nrc_positive REAL, -- Changed from INTEGER to REAL
    nrc_sadness REAL, -- Changed from INTEGER to REAL
    nrc_surprise REAL, -- Changed from INTEGER to REAL
    nrc_trust REAL, -- Changed from INTEGER to REAL
    textblob_polarity REAL,
    textblob_subjectivity REAL,
    vader_neg REAL,
    vader_neu REAL,
    vader_pos REAL,
    vader_compound REAL
);

-- Optional: Add an index for faster lookups if you frequently query by musicbrainz_id
CREATE INDEX idx_lyrics_sentiments_musicbrainz_id ON lyrics_sentiments (musicbrainz_id);

COPY lyrics_sentiments FROM 'C:\Users\robot\Desktop\Music-Recommendation-Engine\backup\lyrics_sentiments\lyrics_analysis.csv' WITH (FORMAT CSV, HEADER TRUE);
