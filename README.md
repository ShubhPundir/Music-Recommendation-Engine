# Music Recommendation Engine

A comprehensive music recommendation system that combines ETL pipelines, sentiment analysis, audio feature extraction, and machine learning models to provide intelligent music recommendations.

## Table of Contents

- [Overview](#overview)
- [ETL and Data Fetching Process](#etl-and-data-fetching-process)
- [Machine Learning & Deep Learning Models](#machine-learning--deep-learning-models)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Database Schema](#database-schema)
- [Usage](#usage)
- [API Integrations](#api-integrations)

## Overview

This project is a full-stack music recommendation engine that:
- Fetches music metadata from multiple APIs (Last.fm, MusicBrainz, Genius)
- Extracts and analyzes audio features using librosa
- Performs sentiment analysis on lyrics using multiple models
- Generates spectrograms and stores them in S3
- Implements various ML/DL models for music recommendation
- Stores data in both MongoDB (NoSQL) and CockroachDB (SQL)

## ETL and Data Fetching Process

### 1. Initial Data Compilation
We compiled a list of **60 albums** and their corresponding artists, stored in `loader/Albums - Sheet1.csv` and `loader/Albums - Sheet2.csv`.

### 2. API Data Fetching
The system loops through the 60 albums and their artists to fetch comprehensive information from three APIs:
- **Last.fm API**: Album metadata, artist information, wiki content, tags
- **MusicBrainz API**: Artist IDs, track metadata, recording information
- **Genius API**: Song lyrics and annotations

This process generates the following database tables:
- `albums` (MongoDB)
- `artists` (MongoDB)
- `tracks_metadata` (MongoDB) - Contains all tracks in each album, with references to albums and artists tables
- `lyrics` (CockroachDB) - Stores lyrics from Genius API

### 3. Sentiment Analysis
Using multiple local static sentiment models, we analyze lyrics to create the `lyrics_sentiments` table (CockroachDB). The models used are:
- **Go Emotions**: BERT-based model (`monologg/bert-base-cased-goemotions-original`) that detects 27 emotion categories
- **VADER**: Rule-based sentiment analyzer for social media text
- **NRC Lexicon**: Emotion lexicon that maps words to 8 basic emotions (anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust)
- **TextBlob**: Simple sentiment analysis providing polarity and subjectivity scores

### 4. Audio Processing Pipeline
To extract audio features, the system:
- Uses **yt-dlp** API to search YouTube and download audio buffers directly to RAM
- Processes audio in-memory using **librosa** Python module to extract comprehensive audio features
- Stores YouTube link references in the `track_links` table (CockroachDB)
- Creates the `audio_features` table (CockroachDB) with features including:
  - **Temporal features**: Tempo, tempo variability, duration, sample rate
  - **Spectral features**: Spectral centroid, rolloff, bandwidth, flatness, contrast
  - **MFCC features**: 13 Mel-frequency cepstral coefficients
  - **Chroma features**: 12 chroma CENS features
  - **Tonal features**: Tonnetz (6 features)
  - **Energy features**: RMS energy, loudness, dynamic range
  - **Spotify-like features**: Danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence
  - **Pitch features**: F0 mean (fundamental frequency)

### 5. WAV and Spectrogram Storage
In parallel to audio feature extraction:
- Each song's audio is saved as a `.wav` file
- Spectrograms are generated from the audio files
- Both `.wav` files and spectrograms are stored in **S3 storage** for later use in deep learning models

### 6. Data Flow Summary
```
CSV Albums List → API Fetching (Last.fm, MusicBrainz, Genius)
    ↓
MongoDB (albums, artists, tracks_metadata) + CockroachDB (lyrics)
    ↓
Sentiment Analysis (Go Emotions, VADER, NRC, TextBlob)
    ↓
CockroachDB (lyrics_sentiments)
    ↓
YouTube Audio Download (yt-dlp) → RAM Buffer
    ↓
Audio Feature Extraction (librosa) → CockroachDB (audio_features)
    ↓
WAV + Spectrogram Generation → S3 Storage
```

## Machine Learning & Deep Learning Models

### 1. Clustering-Based Recommendations (`recommendation/Clustering.ipynb`)

The clustering approach groups similar songs using multiple algorithms:

#### K-Means Clustering
- Clusters songs into 10 groups based on combined audio and sentiment features
- Uses StandardScaler for feature normalization
- Recommendation function finds similar songs within the same cluster using cosine similarity

#### Spectral Clustering
- Uses spectral clustering algorithm for non-convex cluster shapes
- Better at capturing complex relationships in the feature space
- Includes recommendation function: `recommend_from_spectral_cluster(song_id, top_n=5)`

#### Hierarchical Clustering
- Agglomerative clustering with Ward linkage
- Creates a dendrogram structure for song relationships
- Recommendation function: `recommend_from_hierarchical_cluster(song_id, top_n=5)`

#### DBSCAN Clustering
- Density-based clustering that can identify noise points
- Handles outliers better than K-Means
- Recommendation function: `recommend_from_dbscan(song_id, top_n=5)`

**Features Used:**
- Audio features: tempo, energy, danceability, spectral features, MFCCs, chroma, etc.
- Sentiment features: Go Emotions (27), NRC (8), VADER (4), TextBlob (2)
- Total: ~105 features per song

### 2. TF-IDF Based Recommendations (`recommendation/TFIDF.ipynb`)

- Uses **Term Frequency-Inverse Document Frequency** to vectorize lyrics and metadata
- Combines TF-IDF features with audio and sentiment features
- Computes cosine similarity matrix for all songs
- Recommendation function: `recommend(track_id, top_n=5)`

**Text Sources:**
- Genius lyrics
- Last.fm wiki summary
- Last.fm wiki content

### 3. Word2Vec Based Recommendations (`recommendation/Word2Vec.ipynb`)

- Trains a **Word2Vec model** on song lyrics corpus
- Generates word embeddings and aggregates them to create song-level embeddings
- Combines Word2Vec embeddings with audio and sentiment features
- Uses cosine similarity for recommendations
- Model saved as: `recommendation/word2vec_lyrics.model`
- Recommendation function: `recommend(song_index, top_n=5)`

### 4. Deep Learning: CNN for Spectrogram Classification (`deep_learning_notebooks/CNN_ARCHITECTURES_SPECTROGRAMS_LABELS.ipynb`)

A convolutional neural network that classifies music genres from spectrograms:

- **Input**: Spectrogram images (250x100 pixels, RGB)
- **Architecture**: CNN with data augmentation (brightness, contrast, horizontal/vertical shifts)
- **Task**: Multi-label classification (8 genre categories)
- **Genres**: 
  - `blues-r&b-soul`
  - `electronic-funk-disco-dance`
  - `folk-classical-country-jazz`
  - `hip_hop-rap`
  - `opera-musical-theater-soundtrack-vocal-a_cappella`
  - `others`
  - `pop`
  - `rock-metal-psychedelic`
- **Training**: 65 epochs with train/validation/test splits (70%/15%/15%)
- **Output**: `spectrogram_multilabel.h5` model file

**Data Pipeline:**
- Loads spectrograms from S3/local storage
- Uses MultiLabelBinarizer for multi-label encoding
- TensorFlow/Keras implementation with data augmentation

## Project Structure

```
Music-Recommendation-Engine/
├── analysis/                    # Data analysis notebooks
│   ├── Cockroach_Analysis.ipynb
│   ├── Mongo_Analysis.ipynb
│   ├── NLP Lyrical Analysis.ipynb
│   └── spectral_features_analysis_.ipynb
│
├── backup/                      # Database backups and exports
│   ├── albums/
│   ├── artists/
│   ├── audio_features/
│   ├── lyrics/
│   └── track_links/
│
├── database/                    # Database connection modules
│   ├── cockroachdb.py          # CockroachDB connection
│   └── mongodb.py              # MongoDB connection
│
├── deep_learning_notebooks/     # DL models
│   └── CNN_ARCHITECTURES_SPECTROGRAMS_LABELS.ipynb
│
├── docs/                        # Documentation
│   ├── API/                     # API documentation
│   ├── Load/                    # Loading scripts documentation
│   └── SetupReadME.md
│
├── fetchDataApi/                # API integration modules
│   ├── genius.py               # Genius API client
│   ├── last_fm.py              # Last.fm API client
│   ├── musicbrainz.py          # MusicBrainz API client
│   └── track_lyrics_metadata.py # Unified track metadata fetcher
│
├── loader/                      # ETL scripts
│   ├── load-albums-ver0.py     # Load albums from CSV
│   ├── load-artists-ver0.py    # Load artists from CSV
│   ├── load-track-lyrics-ver0.py # Load lyrics
│   ├── load-track_links-audio_features.py # Audio processing
│   ├── load-lyrics_sentiment.py # Sentiment analysis
│   └── load-track-reference.py  # Track reference table
│
├── recommendation/              # ML recommendation models
│   ├── Clustering.ipynb        # Clustering algorithms
│   ├── TFIDF.ipynb             # TF-IDF recommendations
│   ├── Word2Vec.ipynb          # Word2Vec recommendations
│   ├── data/                   # Processed datasets
│   └── word2vec_lyrics.model   # Trained Word2Vec model
│
├── sentiment_analysis/          # Sentiment analysis modules
│   ├── go_emotions.py          # Go Emotions BERT model
│   ├── nrc_lexicon.py          # NRC Lexicon analyzer
│   ├── text_blob.py            # TextBlob analyzer
│   └── vader.py                # VADER analyzer
│
├── spark/                       # Spark processing notebooks
│   ├── PySpark_CockroachDB_Final (1).ipynb
│   └── Spark-MLLib.ipynb
│
├── spectrogram_audio_files_helper/ # Spectrogram utilities
│   └── helper.py
│
├── wavScripts/                  # Audio processing scripts
│   ├── analyzer.py             # Audio feature extraction
│   ├── audio_pipeline.py       # Audio download pipeline
│   └── download_track_via_url.py # YouTube downloader
│
├── scripts/                     # Utility scripts
│   ├── cleansing_tags.py       # Tag normalization
│   └── migration/              # Database migration scripts
│
├── utils/                       # Utility modules
│   └── logger_setup.py         # Logging configuration
│
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites

1. **Python 3.10+**
2. **FFmpeg** installed and available in PATH
   - Windows: Download from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
   - Add `bin/` folder to System PATH
   - Test: `ffmpeg -version`

### Installation

1. **Install `uv` package manager:**
   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Or via pipx:
   ```sh
   pipx install uv
   ```

2. **Create virtual environment and sync dependencies:**
   ```sh
   uv venv
   uv sync
   ```

3. **Activate virtual environment:**
   - **Linux/macOS:**
     ```sh
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```sh
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```sh
     .venv\Scripts\activate.bat
     ```

4. **Create `.env` file** in the root directory:
   ```dotenv
   LASTFM_API_KEY="your_lastfm_api_key"
   GENIUS_ACCESS_TOKEN="your_genius_access_token"
   MUSICBRAINZ_USER_AGENT="your_user_agent_string"
   
   MONGO_ATLAS_URI="your_mongodb_connection_uri"
   
   COCKROACH_USER="your_cockroach_user"
   COCKROACH_PASS="your_cockroach_password"
   COCKROACH_HOST="your_cockroach_host"
   COCKROACH_PORT="your_cockroach_port"
   ```

### Obtaining API Keys

- **Last.fm API Key**: Sign up at [https://www.last.fm/api](https://www.last.fm/api)
- **Genius Access Token**: Register at [https://genius.com/developers](https://genius.com/developers)
- **MusicBrainz User Agent**: Format: `"YourAppName/Version (your-email@example.com)"`
- **MongoDB Atlas URI**: Create cluster at [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- **CockroachDB Credentials**: Sign up at [https://www.cockroachlabs.com/get-started-cockroachdb/](https://www.cockroachlabs.com/get-started-cockroachdb/)

## Database Schema

### MongoDB Collections

#### `albums`
- Album metadata from Last.fm
- References to tracks

#### `artists`
- Artist information from Last.fm
- MusicBrainz artist IDs

#### `tracks_metadata`
- Track information from all APIs
- References to albums and artists
- Last.fm tags (raw and cleaned)
- `final_tags`: Normalized genre tags (JSONB)

### CockroachDB Tables

#### `lyrics`
- `musicbrainz_id` (PRIMARY KEY)
- `genius_lyrics`
- `genius_url`
- `lastfm_wiki_summary`
- `lastfm_wiki_content`

#### `lyrics_sentiments`
- `musicbrainz_id` (PRIMARY KEY)
- Go Emotions: 27 columns (goemotion_sadness, goemotion_love, etc.)
- NRC Lexicon: 8 columns (nrc_anger, nrc_joy, etc.)
- TextBlob: `textblob_polarity`, `textblob_subjectivity`
- VADER: `vader_neg`, `vader_neu`, `vader_pos`, `vader_compound`

#### `audio_features`
- `musicbrainz_id` (PRIMARY KEY)
- Temporal: `duration_seconds`, `sample_rate`, `tempo`, `tempo_variability`
- Energy: `loudness`, `rms_energy`, `dynamic_range`
- Spotify-like: `danceability`, `energy`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`
- Spectral: `spectral_centroid`, `spectral_rolloff`, `spectral_bandwidth`, `spectral_flatness`, `spectral_contrast_1` through `spectral_contrast_7`
- MFCC: `mfcc_1` through `mfcc_13`
- Chroma: `chroma_cens_1` through `chroma_cens_12`
- Tonal: `tonnetz_1` through `tonnetz_6`
- Pitch: `f0_mean`, `mel_mean`
- Other: `zero_crossing_rate`

#### `track_links`
- `musicbrainz_id` (PRIMARY KEY)
- `track_title`
- `channel` (YouTube channel)
- `webpage_url` (YouTube URL)

#### `track_reference`
- `musicbrainz_id` (PRIMARY KEY)
- `title`
- `artist`
- `album`
- Other track metadata

## Usage

### Running ETL Pipelines

1. **Load Albums:**
   ```sh
   python loader/load-albums-ver0.py
   ```

2. **Load Artists:**
   ```sh
   python loader/load-artists-ver0.py
   ```

3. **Load Track Lyrics:**
   ```sh
   python loader/load-track-lyrics-ver0.py
   ```

4. **Load Sentiment Analysis:**
   ```sh
   python loader/load-lyrics_sentiment.py
   ```

5. **Load Audio Features:**
   ```sh
   python loader/load-track_links-audio_features.py
   ```

### Running ML/DL Models

1. **Clustering Recommendations:**
   - Open `recommendation/Clustering.ipynb`
   - Run all cells to generate recommendations

2. **TF-IDF Recommendations:**
   - Open `recommendation/TFIDF.ipynb`
   - Run all cells

3. **Word2Vec Recommendations:**
   - Open `recommendation/Word2Vec.ipynb`
   - Run all cells

4. **CNN Spectrogram Classification:**
   - Open `deep_learning_notebooks/CNN_ARCHITECTURES_SPECTROGRAMS_LABELS.ipynb`
   - Upload spectrogram data and run

### Tag Cleansing

Normalize and clean Last.fm tags:
```sh
python scripts/cleansing_tags.py
```

## API Integrations

### Last.fm API
- Fetches album metadata, artist information, wiki content, and tags
- Module: `fetchDataApi/last_fm.py`

### MusicBrainz API
- Retrieves artist IDs and track metadata
- Module: `fetchDataApi/musicbrainz.py`

### Genius API
- Fetches song lyrics and annotations
- Module: `fetchDataApi/genius.py`

### YouTube (yt-dlp)
- Downloads audio from YouTube videos
- Processes audio in-memory for feature extraction
- Module: `wavScripts/download_track_via_url.py`

## Key Technologies

- **Python 3.10+**
- **MongoDB**: NoSQL database for metadata
- **CockroachDB**: SQL database for structured data
- **librosa**: Audio feature extraction
- **yt-dlp**: YouTube audio download
- **Transformers**: Go Emotions BERT model
- **scikit-learn**: Clustering, TF-IDF, similarity metrics
- **Gensim**: Word2Vec embeddings
- **TensorFlow/Keras**: CNN for spectrogram classification
- **PySpark**: Big data processing (optional)

## License

[Add your license here]

## Contributors

[Add contributors here]

