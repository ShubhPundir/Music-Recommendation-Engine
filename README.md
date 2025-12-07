<h1 align="center"> Music-Recommendation-Engine - ML + DL + BigData </h1>
<p align="center"> The Next Generation of Discovery: Multi-Modal Music Recommendation through Deep Lyrical and Waveform Analysis </p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge">
  <img alt="Issues" src="https://img.shields.io/badge/Issues-0%20Open-blue?style=for-the-badge">
  <img alt="Contributions" src="https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>
<!-- 
  **Note:** These are static placeholder badges. Replace them with your project's actual badges.
  You can generate your own at https://shields.io
-->

## 🗂️ Table of Contents
*   [✨ Overview](#-overview)
*   [🚀 Key Features](#-key-features)
*   [🛠️ Tech Stack & Architecture](#-tech-stack--architecture)
*   [📁 Project Structure](#-project-structure)
*   [📦 Getting Started](#-getting-started)
*   [🔧 Usage](#-usage)
*   [🤝 Contributing](#-contributing)
*   [📝 License](#-license)

---

## ✨ Overview

The **Music-Recommendation-Engine** is a sophisticated data processing and machine learning project designed to create highly granular and contextually rich music recommendations. Unlike traditional systems that rely solely on collaborative filtering or basic genre tags, this engine employs a **multi-modal approach** that deeply analyzes two fundamental components of music: the emotional and thematic content of **lyrics (NLP)** and the intrinsic characteristics of the **audio signal (Waveform Analysis)**.

The project incorporates robust data ingestion pipelines, large-scale data processing capabilities using Spark, and multiple machine learning models (both statistical and deep learning) to derive meaning from raw music data.

### The Problem

> Current music recommendation systems often fall short by relying on simplistic user history or generalized genre classification. They frequently miss the nuance of a song—the complex emotional landscape conveyed by the lyrics, or the unique spectral characteristics of the instrumentation. This leads to repetitive, shallow, and predictable recommendations that fail to capture a user's true mood or artistic preference. The challenge lies in unifying disparate, high-dimensional datasets (text and audio features) into a coherent, actionable model.

### The Solution

The **Music-Recommendation-Engine** solves this by establishing a comprehensive data pipeline that ingests, cleanses, analyzes, and models music data across various dimensions:

1.  **Lyrical Intelligence:** Utilizes multiple state-of-the-art NLP techniques (VADER, GoEmotions, TextBlob, NRC Lexicon, LDA, Word2Vec) to classify lyrics by emotion, sentiment, and thematic topic.
2.  **Acoustic Fingerprinting:** Extracts detailed waveform features (spectral centroid, chroma, MFCCs, etc.) using signal processing tools to quantify the sonic quality of the music.
3.  **Unified Modeling:** Combines these high-fidelity features using Clustering, Spark MLLib, and custom Deep Learning (CNN on spectrograms) approaches to generate robust recommendation vectors.

### Architecture Overview

The system operates as an end-to-end data pipeline: data is scraped from external APIs (Genius, MusicBrainz, Last.fm), stored and managed in a hybrid database environment (MongoDB for raw data, CockroachDB/Postgres for relational analysis), processed through dedicated loading and migration scripts, and finally fed into the `recommendation` and `spark` modules for advanced modeling and analysis. Core services rely on `ffmpeg` and `yt-dlp` for efficient audio handling and downloading.

---

## 🚀 Key Features

The engine is built on robust data science methodologies, offering unparalleled depth in music analysis and recommendation.

### 🧠 Deep Lyrical Intelligence

*   **Emotional Context Mapping:** Utilizes specialized lexicons (`NRC-Emotion-Lexicon`) and pre-trained models (`go_emotions`, `vader`, `text_blob`) to precisely map the emotional landscape of song lyrics (e.g., Joy, Anger, Sadness, Anticipation).
*   **Thematic Topic Discovery (LDA):** Runs Latent Dirichlet Allocation (LDA) to create pseudo-documents from lyrical chunks, enabling sophisticated extraction of high-level themes and topics for content-based filtering.
*   **Word Embeddings (Word2Vec):** Generates and utilizes custom Word2Vec models trained on lyric corpora to understand semantic relationships between words, enhancing the accuracy of content similarity matching.
*   **Genius Annotations:** Scrapes and processes data from the Genius API, providing access to deeper lyrical meaning and contextual annotations.

### 🔊 Advanced Audio Analysis

*   **Waveform Feature Extraction:** Executes signal processing scripts (`waveform_features.py`, `analyzer.py`) to extract essential acoustic features like Mel-Frequency Cepstral Coefficients (MFCCs), spectral characteristics, and rhythmic patterns directly from audio buffers.
*   **Spectrogram Deep Learning:** Incorporates notebooks and models (`CNN_ARCHITECTURES_SPECTROGRAMS_LABELS.ipynb`) dedicated to training Convolutional Neural Networks (CNNs) on visual spectrogram representations of audio, enabling label prediction and feature learning based purely on audio structure.
*   **Robust Audio Pipeline:** Features specialized scripts for handling complex audio operations, including downloading audio streams via URL (`download_track_via_url.py`) and robust logging/error handling for high-volume data ingestion.

### ⚙️ Scalable Data Infrastructure

*   **Hybrid Database System:** Leverages MongoDB for flexible storage of raw metadata and CockroachDB/Postgres for transactional stability, relational queries, and large-scale data migrations.
*   **Big Data Processing (PySpark):** Integrates PySpark for efficient querying and processing of large datasets stored in CockroachDB, specifically leveraging Spark MLlib for high-performance clustering and recommendation model training.
*   **Automated Data Migration:** Dedicated scripts (`mongo2psql_*.py`) handle the transformation and migration of raw metadata from MongoDB into the normalized relational schema in CockroachDB/Postgres.

### 🔗 Comprehensive Metadata Acquisition

*   **Multi-Source API Integration:** Seamlessly retrieves enriched track, artist, and album metadata by connecting to industry-leading sources including MusicBrainz, Genius, and Last.fm, ensuring high data integrity and depth.
*   **Data Cleansing and Integrity:** Includes specialized scripts (`cleansing_tags.py`) for normalizing and cleansing raw data, particularly handling the variability and ambiguity of tags sourced from external APIs like Last.fm.

---

## 🛠️ Tech Stack & Architecture

This project is built using a robust set of open-source libraries focused on data manipulation, signal processing, and high-performance database connectivity, primarily relying on the Python ecosystem.

| Technology | Purpose | Why it was Chosen |
| :--- | :--- | :--- |
| **Python 3.10** | Core programming language environment. | Provides extensive libraries for ML/DL, NLP, and data processing. |
| **beautifulsoup4** | HTML parsing and web scraping. | Essential for reliably extracting lyrical content from web pages (e.g., Genius). |
| **dotenv** | Environment variable management. | Securely loads configuration variables for API keys and database connections. |
| **ffmpeg** | Multimedia handling and conversion. | Crucial for decoding and processing various audio formats into analyzable streams. |
| **ffprobe** | Audio/video stream analysis utility. | Used alongside `ffmpeg` to gather detailed metadata about audio files before processing. |
| **numpy** | Fundamental package for scientific computing. | Core dependency for all numerical operations, array manipulation, and signal processing. |
| **psycopg2** | PostgreSQL adapter for Python. | Enables secure and efficient connectivity to CockroachDB (Postgres-compatible) for transactional data. |
| **pymongo** | Official MongoDB driver for Python. | Facilitates fast, flexible access and management of raw, unstructured metadata in MongoDB. |
| **requests** | HTTP library for making API calls. | Used for fetching metadata from Last.fm, MusicBrainz, and Genius APIs. |
| **yt-dlp** | Video/audio downloading utility. | Critical tool for reliably sourcing and streaming audio tracks from URLs into the processing pipeline. |

---

## 📁 Project Structure

The repository is logically organized to separate data pipelines, analysis notebooks, core recommendation logic, and external API fetching utilities.

```
📂 ShubhPundir-Music-Recommendation-Engine-a00342b/
├── 📄 .python-version               # Specifies required Python version (3.10)
├── 📄 requirements.txt              # List of Python dependencies
├── 📄 main.py                       # Main application entry point
├── 📂 analysis/                     # Jupyter notebooks for data exploration and insights
│   ├── 📄 spectral_features_analysis_.ipynb
│   ├── 📄 NLP Lyrical Analysis.ipynb
│   └── 📄 Cockroach_Analysis.ipynb
├── 📂 backup/                       # Database dumps, raw data snapshots, and historical references
│   ├── 📄 mre.sql
│   ├── 📂 tracks_metadata/
│   │   └── 📄 music.tracks_metadata.json
│   └── 📂 audio_features/
│       └── 📄 audio_features_202505061902.csv
├── 📂 database/                     # Database connection and utility modules
│   ├── 📄 mongodb.py                # MongoDB connection handler
│   └── 📄 cockroachdb.py            # CockroachDB/Postgres connection handler
├── 📂 deep_learning_notebooks/      # Notebooks dedicated to advanced DL models
│   └── 📄 CNN_ARCHITECTURES_SPECTROGRAMS_LABELS.ipynb
├── 📂 docs/                         # Documentation for APIs, pipelines, and sentiment analysis
│   ├── 📂 API/                      # External API route documentation
│   │   ├── 📄 API-default.md
│   │   ├── 📂 Genius/
│   │   └── 📂 Musicbrainz/
│   └── 📂 WAVScripts/               # Audio processing script documentation
│       └── 📄 audio_pipeline.md
├── 📂 fetchDataApi/                 # Modules for scraping and fetching external metadata
│   ├── 📄 musicbrainz.py
│   ├── 📄 genius.py
│   ├── 📄 last_fm.py
│   └── 📄 geniusAnnotator.py        # Logic for processing lyrical annotations
├── 📂 loader/                       # Scripts responsible for loading processed data into the database
│   ├── 📄 load-track_links-audio_features.py
│   ├── 📄 load_audio_spectro.py
│   ├── 📄 load-lyrics_sentiment.py
│   ├── 📄 load-albums-ver0.py
│   ├── 📄 generate_metadata.py
│   ├── 📂 removing-duplicates-unreferrenced/
│   │   └── 📄 removing duplicates.py
│   └── 📂 Pipeline debugging track_links-audio_features/ # Specific RAM error handling scripts
│       ├── 📄 RAM-Buffer-Overflow.py
│       └── 📄 RAM-Buffer-Underflow.py
├── 📂 logs/                         # Historical log files from pipeline runs
│   ├── 📂 audio-pipeline/
│   │   └── 📂 Regular-Runs/
│   │       ├── 📂 alpha/
│   │       └── 📂 beta/
│   └── 📂 track-lyrics/
│       ├── 📂 2/
│       └── 📂 1/
├── 📂 recommendation/               # Core recommendation modeling artifacts and notebooks
│   ├── 📄 word2vec_lyrics.model     # Pre-trained Word2Vec model
│   ├── 📄 Word2Vec.ipynb
│   ├── 📄 TFIDF.ipynb
│   ├── 📄 Clustering.ipynb
│   └── 📂 data/
│       ├── 📄 audio_features.csv
│       └── 📄 lyrics_emotions.csv
├── 📂 scripts/                      # Utility scripts, data cleansing, and migration tools
│   ├── 📄 cleansing_tags.py         # Cleanses and normalizes LastFM tags
│   └── 📂 migration/                # Scripts for migrating MongoDB data to relational storage
│       ├── 📄 mongo2psql_tracks_metadata.py
│       ├── 📄 mongo2psql_artists.py
│       └── 📄 mongo2psql_albums.py
├── 📂 sentiment_analysis/           # Modules for multi-faceted text sentiment and emotion analysis
│   ├── 📄 go_emotions.py            # GoEmotions analysis implementation
│   ├── 📄 text_blob.py              # TextBlob analysis implementation
│   ├── 📄 vader.py                  # VADER analysis implementation
│   ├── 📄 nrc_lexicon.py            # NRC Lexicon implementation
│   └── 📄 NRC-Emotion-Lexicon-Wordlevel-v0.92.txt # Emotion lexicon file
├── 📂 setup/                        # Scripts for initial environment configuration
│   ├── 📄 setup_ffmpeg.py           # Sets up required FFmpeg dependencies
│   └── 📄 check_ffmpeg.py
├── 📂 spark/                        # PySpark and Big Data related scripts and notebooks
│   ├── 📄 Spark-MLLib.ipynb         # Notebook demonstrating MLlib usage
│   ├── 📄 PySpark_CockroachDB_Final (1).ipynb
│   └── 📄 spark_db_query.py
├── 📂 spectrogram_audio_files_helper/ # Helper utilities for handling spectrogram images
│   └── 📄 helper.py
├── 📂 test/                         # Unit tests and analysis test environments
│   ├── 📂 embeddings/
│   │   ├── 📄 all.py                # Comprehensive text analysis runner
│   │   └── 📄 NRC-Emotion-Lexicon-Wordlevel-v0.92.txt
│   └── 📂 waveform features/        # Scripts for audio feature testing
│       └── 📄 waveform_features.py
├── 📂 utils/                        # General utilities
│   └── 📄 logger_setup.py           # Standardized logger configuration
└── 📂 wavScripts/                   # Core audio processing and download scripts
    ├── 📄 analyzer.py               # Extracts audio features from memory buffer
    ├── 📄 download_track_via_url.py # Handles streaming and downloading audio
    └── 📄 audio_pipeline.py         # Main orchestration of the audio processing pipeline
```

---

## 📦 Getting Started

This section outlines the minimal steps required to set up the local development environment and satisfy the core dependencies.

### Prerequisites

The project requires a specific Python environment and relies on system-level multimedia processing tools, which are managed by the provided setup scripts.

*   **Python:** Version `3.10` is required for dependency compatibility.
*   **System Tools:** `ffmpeg` and `ffprobe` are essential for audio processing.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ShubhPundir-Music-Recommendation-Engine-a00342b
    cd ShubhPundir-Music-Recommendation-Engine-a00342b
    ```

2.  **Set up the Python Environment:**

    It is highly recommended to use a virtual environment (e.g., `venv` or `conda`):

    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies:**

    Install the project dependencies using `pip`. Note that the project relies heavily on data science libraries like `numpy` and utility tools like `yt-dlp`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure FFmpeg (Optional but Recommended):**

    The project includes a utility script to help install and configure the necessary audio processing tools, `ffmpeg` and `ffprobe`.

    ```bash
    python setup/setup_ffmpeg.py
    python setup/check_ffmpeg.py
    ```
    This ensures that the `wavScripts/audio_pipeline.py` can correctly decode and analyze audio streams.

---

## 🔧 Usage

The Music Recommendation Engine is primarily used by executing data ingestion pipelines, running migration scripts, and performing advanced analysis within the provided Jupyter notebooks.

### 1. Data Ingestion and Pipeline Execution

The system uses dedicated loader and pipeline scripts to fetch metadata, download audio, and calculate features.

**A. Running the Audio Pipeline:**

To start the process of fetching audio tracks from external URLs, downloading the audio stream to memory, analyzing waveform features, and inserting the results into the database, use the primary audio pipeline module.

```bash
# Example: Executing the main audio feature extraction pipeline
python wavScripts/audio_pipeline.py
```

**B. Loading Track Metadata:**

Scripts in the `loader/` directory handle batch insertion of data collected from APIs into the relational database:

```bash
# Example: Running the loader for track links and audio features
python loader/load-track_links-audio_features.py

# Example: Loading lyrics and performing sentiment analysis afterwards
python loader/load-track-lyrics-ver0.py
python loader/load-lyrics_sentiment.py
```

### 2. Data Migration

If you are transitioning from a raw MongoDB data store to the CockroachDB analytical store, use the migration scripts found in `scripts/migration`:

```bash
# Migrate tracks metadata from MongoDB to CockroachDB
python scripts/migration/mongo2psql_tracks_metadata.py

# Migrate artist data
python scripts/migration/mongo2psql_artists.py
```

### 3. Running Advanced Analysis & Modeling

The core recommendation models and deep-dive analysis are conducted within the Jupyter notebooks located in the `analysis/`, `recommendation/`, and `spark/` directories.

To launch the Jupyter environment:

```bash
jupyter notebook
```

**Key Notebooks for Model Training:**

| Notebook Path | Focus | Outcome |
| :--- | :--- | :--- |
| `recommendation/Word2Vec.ipynb` | Training word embeddings on the lyric dataset. | Generates `word2vec_lyrics.model` for semantic search. |
| `recommendation/Clustering.ipynb` | Applying unsupervised learning to feature vectors. | Identifies natural clusters in the combined feature space (audio + lyrical). |
| `spark/Spark-MLLib.ipynb` | Leveraging distributed computing for model scaling. | Demonstrates scalable machine learning using PySpark MLlib for recommendation tasks. |
| `deep_learning_notebooks/CNN_ARCHITECTURES_SPECTROGRAMS_LABELS.ipynb` | Building Deep Learning models for audio classification. | Trains CNNs on spectrogram images to predict labels or extract deep audio features. |

---

## 🤝 Contributing

We welcome contributions to improve the **Music-Recommendation-Engine**! Your input helps make this project better for everyone.

### How to Contribute

1. **Fork the repository** - Click the 'Fork' button at the top right of this page
2. **Create a feature branch** 
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** - Improve code, documentation, or features (e.g., optimizing feature extraction in `analyzer.py`, or adding a new sentiment model).
4. **Test thoroughly** - Ensure all functionality works as expected. Given the nature of this ML/Data project, testing often involves pipeline integrity and data validation checks.
   ```bash
   # Example of running a specific test module
   python fetchDataApi/test/main_test.py
   ```
5. **Commit your changes** - Write clear, descriptive commit messages
   ```bash
   git commit -m 'Feat: Implement improved sentiment analysis using new library X'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** - Submit your changes for review against the main branch.

### Development Guidelines

- ✅ Follow the existing code style and conventions, particularly within the pipeline (`loader/`, `wavScripts/`).
- 📝 Add comments for complex logic and algorithms (e.g., feature weighting in recommendation notebooks).
- 🧪 Write tests for new features and bug fixes (especially for new API fetching or data migration logic).
- 📚 Update documentation in the `docs/` folder for any changed functionality or new API routes.
- 🔄 Ensure backward compatibility when modifying core data models or migration scripts.
- 🎯 Keep commits focused and atomic.

### Ideas for Contributions

We're looking for help with:

- 🐛 **Bug Fixes:** Address issues related to external API rate limits or data corruption during migrations.
- ✨ **New Features:** Implement new recommendation algorithms (e.g., Matrix Factorization) or integrate a new data source API.
- 📖 **Documentation:** Improve README, add tutorials for setting up CockroachDB/MongoDB connections, or elaborate on the Spark integration.
- ⚡ **Performance:** Optimize resource usage in RAM-intensive scripts found in `loader/Pipeline debugging...`.
- 🧪 **Testing:** Increase test coverage for the `fetchDataApi/` modules.

### Code Review Process

- All submissions require review before merging by the project maintainer.
- Maintainers will provide constructive feedback based on architectural coherence and accuracy.
- Changes may be requested before approval.
- Once approved, your PR will be merged and you'll be credited.

### Questions?

Feel free to open an issue for any questions or concerns. We're here to help!

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for complete details.

### What this means:

- ✅ **Commercial use:** You can use this project commercially
- ✅ **Modification:** You can modify the code
- ✅ **Distribution:** You can distribute this software
- ✅ **Private use:** You can use this project privately
- ⚠️ **Liability:** The software is provided "as is", without warranty
- ⚠️ **Trademark:** This license does not grant trademark rights

---

<p align="center">Made with ❤️ by the Shubh Pundir Team</p>
<p align="center">
  <a href="#">⬆️ Back to Top</a>
</p>
