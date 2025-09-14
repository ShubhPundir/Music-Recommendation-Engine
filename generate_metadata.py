import os
import json
from datetime import datetime
from pydub import AudioSegment
import librosa
from PIL import Image

def get_audio_metadata(audio_path):
    audio = AudioSegment.from_file(audio_path)
    y, sr = librosa.load(audio_path, sr=None)
    # Calculate bit rate: (frame_rate * sample_width * channels) in bits per second
    # sample_width is in bytes, so multiply by 8 for bits
    bit_rate = audio.frame_rate * audio.sample_width * 8 * audio.channels
    return {
        "filename": os.path.basename(audio_path),
        "duration_sec": len(audio) / 1000,
        "sample_rate": sr,
        "channels": audio.channels,
        "frame_rate": audio.frame_rate,
        "bit_rate": bit_rate,
        "file_size_bytes": os.path.getsize(audio_path),
        "created_at": datetime.fromtimestamp(os.path.getctime(audio_path)).isoformat()
    }

def get_image_metadata(image_path):
    # Use PIL to get dimensions and channels
    with Image.open(image_path) as img:
        width, height = img.size
        mode = img.mode
        # Channels: 'L'=1, 'RGB'=3, 'RGBA'=4, etc.
        channels = len(img.getbands())
    return {
        "filename": os.path.basename(image_path),
        "dimensions": {"width": width, "height": height},
        "channels": channels,
        "file_size_bytes": os.path.getsize(image_path),
        "created_at": datetime.fromtimestamp(os.path.getctime(image_path)).isoformat()
    }

def collect_wav_metadata(wav_dir, output_json):
    # Collect common fields: channels, bit_rate, sample_rate (if needed)
    channels = None
    bit_rate = None
    for fname in os.listdir(wav_dir):
        if fname.lower().endswith(".wav"):
            fpath = os.path.join(wav_dir, fname)
            try:
                meta = get_audio_metadata(fpath)
                # Use the first file's values as representative
                channels = meta["channels"]
                bit_rate = meta["bit_rate"]
                break
            except Exception as e:
                print(f"Error processing {fpath}: {e}")
    common = {"channels": channels, "bit_rate": bit_rate}
    with open(output_json, "w") as f:
        json.dump(common, f, indent=2)
    print(f"WAV metadata written to {output_json}")

def collect_spectrogram_metadata(img_dir, output_json):
    # Collect common fields: dimensions, channels
    dimensions = None
    channels = None
    for fname in os.listdir(img_dir):
        if fname.lower().endswith(".jpg") or fname.lower().endswith(".png"):
            fpath = os.path.join(img_dir, fname)
            try:
                meta = get_image_metadata(fpath)
                dimensions = meta["dimensions"]
                channels = meta["channels"]
                break
            except Exception as e:
                print(f"Error processing {fpath}: {e}")
    common = {"dimensions": dimensions, "channels": channels}
    with open(output_json, "w") as f:
        json.dump(common, f, indent=2)
    print(f"Spectrogram metadata written to {output_json}")

if __name__ == "__main__":
    # Update these paths as needed
    wav_dir = os.path.join("rec")
    wav_json = os.path.join("rec", "wav_metadata.json")
    img_dir = os.path.join("spectrogram", "file_jpg")
    img_json = os.path.join("spectrogram", "file_jpg", "spectrogram_metadata.json")
    collect_wav_metadata(wav_dir, wav_json)
    collect_spectrogram_metadata(img_dir, img_json)