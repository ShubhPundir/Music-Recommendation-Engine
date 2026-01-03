import subprocess
import sys

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True)
        print("✅ FFmpeg is available.")
        sys.exit(1)
    except Exception:
        print("❌ FFmpeg is not installed or not in PATH.")

if __name__ == "__main__":
    check_ffmpeg()
