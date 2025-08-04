import subprocess
import sys

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True)
        print("✅ FFmpeg is available.")
    except Exception:
        print("❌ FFmpeg is not installed or not in PATH.")
        sys.exit(1)

if __name__ == "__main__":
    check_ffmpeg()
