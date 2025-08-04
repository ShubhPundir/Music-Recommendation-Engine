import os
import zipfile
import shutil
import urllib.request
import subprocess
import sys

def download_ffmpeg(download_url, dest_path):
    print("⬇️ Downloading FFmpeg...")
    urllib.request.urlretrieve(download_url, dest_path)
    print("✅ Downloaded FFmpeg zip.")

def extract_ffmpeg(zip_path, extract_to):
    print("📦 Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print("✅ Extracted FFmpeg.")

def add_to_path(bin_path):
    print(f"🔧 Adding {bin_path} to user PATH...")
    import winreg

    env = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
    try:
        current_path, _ = winreg.QueryValueEx(env, 'Path')
    except FileNotFoundError:
        current_path = ''

    if bin_path.lower() not in current_path.lower():
        new_path = f"{current_path};{bin_path}" if current_path else bin_path
        winreg.SetValueEx(env, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
        print("✅ PATH updated. You may need to restart your terminal.")
    else:
        print("ℹ️ FFmpeg path already in PATH.")

def setup_ffmpeg():
    # FFmpeg static Windows build (from gyan.dev)
    ffmpeg_zip_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    install_dir = os.path.abspath("ffmpeg")  # you can change this
    zip_path = os.path.join(install_dir, "ffmpeg.zip")

    os.makedirs(install_dir, exist_ok=True)

    # Step 1: Download
    download_ffmpeg(ffmpeg_zip_url, zip_path)

    # Step 2: Extract
    extract_ffmpeg(zip_path, install_dir)

    # Step 3: Move the correct subfolder (it's like ffmpeg-2023.... -> bin, doc, presets, etc.)
    root_contents = os.listdir(install_dir)
    extracted_dir = next((d for d in root_contents if os.path.isdir(os.path.join(install_dir, d)) and "ffmpeg" in d), None)

    if extracted_dir:
        ffmpeg_root = os.path.join(install_dir, extracted_dir)
        for item in os.listdir(ffmpeg_root):
            s = os.path.join(ffmpeg_root, item)
            d = os.path.join(install_dir, item)
            if os.path.isdir(s):
                shutil.move(s, d)
        shutil.rmtree(ffmpeg_root)

    # Step 4: Add to PATH
    bin_path = os.path.join(install_dir, "bin")
    add_to_path(bin_path)

    # Step 5: Clean zip
    os.remove(zip_path)

    # Step 6: Confirm
    print("🎬 Verifying FFmpeg installation:")
    subprocess.run(["ffmpeg", "-version"])

if __name__ == "__main__":
    if os.name != "nt":
        print("❌ This installer currently supports only Windows.")
        sys.exit(1)

    setup_ffmpeg()
