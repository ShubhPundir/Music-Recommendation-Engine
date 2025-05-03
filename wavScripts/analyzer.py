import librosa
import numpy as np

def extract_audio_features_for_table(audio_path, track_id, analysis_id):
    y, sr = librosa.load(audio_path, sr=None)

    # Basic Audio Information
    duration_seconds = librosa.get_duration(y=y, sr=sr)
    sample_rate = sr

    # Tempo and Beat
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    # Loudness, Key, Mode, Time Signature (if available)
    onset_env_loudness = librosa.onset.onset_strength(y=y, sr=sr)
    loudness = np.mean(onset_env_loudness)  # Simplified approximation for loudness
    
    # Chroma to estimate key and mode (simplified)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    # Spectral Features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    # MFCCs (first 13 coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)

    # Energy and Zero Crossing Rate (ZCR)
    rms = librosa.feature.rms(y=y)
    energy = np.mean(rms)
    zcr = librosa.feature.zero_crossing_rate(y)
    zcr_mean = np.mean(zcr)

    # Musical Features
    danceability = min(1.0, tempo / 200 + (1 - zcr_mean)) / 2
    acousticness = 1 - zcr_mean
    valence = np.mean(chroma_mean)
    instrumentalness = 1 - np.mean(spectral_centroid) / (np.max(spectral_centroid) + 1e-6)
    speechiness = np.mean(zcr)
    liveness = 0.5  # Placeholder for liveness feature (could be obtained from a model)

    # Prepare the return values as per the SQL schema
    audio_analysis = {
        "analysis_id": analysis_id,
        "track_id": track_id,
        "file_path": audio_path,
        "duration_seconds": duration_seconds,
        "sample_rate": sample_rate,
        "tempo": float(tempo),
        "loudness": float(loudness),
        "danceability": float(danceability),
        "energy": float(energy),
        "speechiness": float(speechiness),
        "acousticness": float(acousticness),
        "instrumentalness": float(instrumentalness),
        "liveness": float(liveness),
        "valence": float(valence),
        "spectral_centroid": float(np.mean(spectral_centroid)),
        "spectral_rolloff": float(np.mean(spectral_rolloff)),
        "spectral_bandwidth": float(np.mean(spectral_bandwidth)),
        "spectral_contrast": spectral_contrast.mean(axis=1).tolist(),
        "zero_crossing_rate": float(zcr_mean),
        "rms_energy": float(energy),
        "mfcc_1": float(mfccs_mean[0]),
        "mfcc_2": float(mfccs_mean[1]),
        "mfcc_3": float(mfccs_mean[2]),
        "mfcc_4": float(mfccs_mean[3]),
        "mfcc_5": float(mfccs_mean[4]),
        "mfcc_6": float(mfccs_mean[5]),
        "mfcc_7": float(mfccs_mean[6]),
        "mfcc_8": float(mfccs_mean[7]),
        "mfcc_9": float(mfccs_mean[8]),
        "mfcc_10": float(mfccs_mean[9]),
        "mfcc_11": float(mfccs_mean[10]),
        "mfcc_12": float(mfccs_mean[11]),
        "mfcc_13": float(mfccs_mean[12]),
    }

    return audio_analysis
