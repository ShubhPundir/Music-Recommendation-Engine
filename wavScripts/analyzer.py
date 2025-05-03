import soundfile as sf
import librosa
import numpy as np

def extract_audio_features_from_buffer(audio_buffer, track_id):
    y, sr = sf.read(audio_buffer)
    y = y.astype(np.float32)
    
    duration_seconds = librosa.get_duration(y=y, sr=sr)
    harmonic, _ = librosa.effects.hpss(y)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    tempo_var = np.std(librosa.feature.rhythm.tempo(onset_envelope=onset_env, sr=sr, aggregate=None))
    loudness = np.mean(onset_env)
    chroma_mean = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)
    chroma_cens = np.mean(librosa.feature.chroma_cens(y=y, sr=sr), axis=1)
    mfccs_mean = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    spectral_flatness = librosa.feature.spectral_flatness(y=y)
    zcr = librosa.feature.zero_crossing_rate(y)
    rms = librosa.feature.rms(y=y)
    tonnetz = librosa.feature.tonnetz(y=harmonic, sr=sr)
    mel_mean = np.mean(librosa.feature.melspectrogram(y=y, sr=sr))
    f0 = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    f0_mean = np.nanmean(f0)

    danceability = min(1.0, tempo / 200 + (1 - np.mean(zcr))) / 2
    acousticness = 1 - np.mean(zcr)
    valence = np.mean(chroma_mean)
    instrumentalness = 1 - np.mean(spectral_centroid) / (np.max(spectral_centroid) + 1e-6)
    speechiness = np.mean(zcr)
    liveness = np.var(rms)
    dynamic_range = np.max(rms) - np.min(rms)

    return {
        "musicbrainz_id": track_id,
        "duration_seconds": duration_seconds,
        "sample_rate": sr,
        "tempo": float(tempo),
        "loudness": float(loudness),
        "danceability": float(danceability),
        "energy": float(np.mean(rms)),
        "speechiness": float(speechiness),
        "acousticness": float(acousticness),
        "instrumentalness": float(instrumentalness),
        "liveness": float(liveness),
        "valence": float(valence),
        "spectral_centroid": float(np.mean(spectral_centroid)),
        "spectral_rolloff": float(np.mean(spectral_rolloff)),
        "spectral_bandwidth": float(np.mean(spectral_bandwidth)),
        "spectral_contrast": spectral_contrast.mean(axis=1).tolist(),
        "spectral_flatness": float(np.mean(spectral_flatness)),
        "zero_crossing_rate": float(np.mean(zcr)),
        "rms_energy": float(np.mean(rms)),
        **{f"mfcc_{i+1}": float(val) for i, val in enumerate(mfccs_mean)},
        "chroma_cens_mean": chroma_cens.tolist(),
        "tonnetz": np.mean(tonnetz, axis=1).tolist(),
        "mel_mean": float(mel_mean),
        "tempo_variability": float(tempo_var),
        "f0_mean": float(f0_mean),
        "dynamic_range": float(dynamic_range),
    }
