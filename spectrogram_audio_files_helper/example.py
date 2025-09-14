import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
from pydub import AudioSegment
import numpy as np

# Output directory for audio and spectrogram images
OUTPUT_DIR = os.path.join("spectrogram")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_audio_file(buf_memory_containing_audio, filename_prefix, output_dir):
    """
    Saves a WAV audio file from memory buffer into the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{filename_prefix}.wav")
    buf_memory_containing_audio.seek(0)
    audio = AudioSegment.from_file(buf_memory_containing_audio, format="wav")
    audio.export(output_path, format="wav")
    print(f"Audio saved at: {output_path}")

def save_spectrogram_image(buf_memory_containing_audio, filename_prefix, output_dir):
    """
    Saves a spectrogram image (.jpg) from memory buffer into the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{filename_prefix}.jpg")
    buf_memory_containing_audio.seek(0)
    y, sr = librosa.load(buf_memory_containing_audio, sr=None)
    S = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)

    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(111)
    img = librosa.display.specshow(S, sr=sr, x_axis=None, y_axis=None, ax=ax)
    # Remove axes, ticks, and labels
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.margins(0, 0)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)
    print(f"Spectrogram saved at: {output_path}")
