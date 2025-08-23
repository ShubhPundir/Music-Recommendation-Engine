import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
from pydub import AudioSegment
import numpy as np

# Output directory for audio and spectrogram images
OUTPUT_DIR = os.path.join("spectrogram", "file_jpg")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_audio_file(buf_memory_containing_audio, filename_prefix):
    """
    Saves a WAV audio file from memory buffer into spectrogram/file_jpg/.
    """
    output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}.wav")
    buf_memory_containing_audio.seek(0)
    audio = AudioSegment.from_file(buf_memory_containing_audio, format="wav")
    audio.export(output_path, format="wav")
    print(f"Audio saved at: {output_path}")

def save_spectrogram_image(buf_memory_containing_audio, filename_prefix):
    """
    Saves a spectrogram image (.jpg) from memory buffer into spectrogram/file_jpg/.
    """
    output_path = os.path.join(OUTPUT_DIR, f"{filename_prefix}.jpg")
    buf_memory_containing_audio.seek(0)
    y, sr = librosa.load(buf_memory_containing_audio, sr=None)
    S = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Spectrogram saved at: {output_path}")
