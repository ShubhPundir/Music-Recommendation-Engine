import librosa
import numpy as np

def extract_all_audio_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    # Tempo and Beat
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Energy
    rms = librosa.feature.rms(y=y)
    energy = np.mean(rms)

    # Zero Crossing Rate (for Acousticness, Danceability)
    zcr = librosa.feature.zero_crossing_rate(y)
    zcr_mean = np.mean(zcr)

    # Spectral Features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)

    # MFCC
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)

    # Chroma
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    # Feature approximations
    danceability = min(1.0, tempo / 200 + (1 - zcr_mean)) / 2
    acousticness = 1 - zcr_mean
    valence = np.mean(chroma_mean)
    instrumentalness = 1 - np.mean(spectral_centroid) / (np.max(spectral_centroid) + 1e-6)
    speechiness = np.mean(zcr)

    return {
        "tempo": float(tempo),
        "energy": float(energy),
        "danceability": float(danceability),
        "acousticness": float(acousticness),
        "valence": float(valence),
        "instrumentalness": float(instrumentalness),
        "speechiness": float(speechiness),
        "zcr_mean": float(zcr_mean),
        "spectral_centroid": float(np.mean(spectral_centroid)),
        "spectral_bandwidth": float(np.mean(spectral_bandwidth)),
        "spectral_rolloff": float(np.mean(spectral_rolloff)),
        "mfccs_mean": mfccs_mean.tolist(),
        "chroma_mean": chroma_mean.tolist(),
    }
