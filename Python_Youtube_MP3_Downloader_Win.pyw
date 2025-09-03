import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox
# last change 02.09.2025
#--- music dir where mp3 file are saved ---
path_music_dir= os.getcwd() + "\\music"
os.makedirs(path_music_dir,exist_ok=True)

# --- yt-dlp Installation---
try:
    import yt_dlp
except ImportError:
    print("yt-dlp not found. Installing it...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp
#--- Download ffmpeg if not present ---
# dir for ffmpeg
ffmpeg_path = os.path.join(os.environ['USERPROFILE'], "ffmpeg")
os.makedirs(ffmpeg_path, exist_ok=True)
bin_path = os.path.join(ffmpeg_path, "bin")
# --- Download ffmpeg if not present ---
ffmpeg_exe = os.path.join(bin_path, "ffmpeg.exe")
ffprobe_exe = os.path.join(bin_path, "ffprobe.exe")
ffplay_exe = os.path.join(bin_path, "ffplay.exe")

if not (os.path.isfile(ffmpeg_exe) and os.path.isfile(ffprobe_exe)and os.path.isfile(ffplay_exe)):
    print("ffmpeg not found. Downloading...")
    zip_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_file = os.path.join(ffmpeg_path, "ffmpeg.zip")

    # Download ZIP
    urllib.request.urlretrieve(zip_url, zip_file)
    print("Download complete. Extracting...")

    # Extract ZIP
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(ffmpeg_path)

    # Find extracted folder
    extracted_folder = None
    for f in os.listdir(ffmpeg_path):
        full_path = os.path.join(ffmpeg_path, f)
        if os.path.isdir(full_path) and f.startswith("ffmpeg"):
            extracted_folder = full_path
            break

    if extracted_folder is None:
        raise Exception("Extracted ffmpeg folder not found!")

    # Path to bin folder inside extracted folder
    extracted_bin = os.path.join(extracted_folder, "bin")
    os.makedirs(bin_path, exist_ok=True)

    # Move all files from extracted bin to target bin
    for file in os.listdir(extracted_bin):
        shutil.move(os.path.join(extracted_bin, file), os.path.join(bin_path, file))

    # Remove temporary files
    os.remove(zip_file)
    shutil.rmtree(extracted_folder)
    print("ffmpeg setup complete.")


#--- Function to download MP3 ---
def download_mp3():
    url = entry_url.get().strip()
    if not url:
        messagebox.showwarning("Input error", "Please enter a YouTube URL")
        return

    success = False

    # --- 1. Try without cookies ---
    try:
        subprocess.run([
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--ffmpeg-location", bin_path,
            "-o", os.path.join(path_music_dir, "%(title)s.%(ext)s"),
            url
        ], creationflags=subprocess.CREATE_NO_WINDOW, check=True)
        success = True
    except subprocess.CalledProcessError:
        pass  # If fail try with cookies
    # --- 2. Try with browser cookies ---
    if not success:
        browsers = ["firefox", "edge", "chrome", "opera", "brave"]
        for browser in browsers:
            try:
                subprocess.run([
                    "yt-dlp",
                    "-x",
                    "--audio-format", "mp3",
                    "--ffmpeg-location", bin_path,
                    "--cookies-from-browser", browser,
                    "-o", os.path.join(path_music_dir, "%(title)s.%(ext)s"),
                    url
                ], creationflags=subprocess.CREATE_NO_WINDOW, check=True)
                success = True
                break
            except subprocess.CalledProcessError:
                continue

    if success:
        messagebox.showinfo("Success", f"Download complete!\nSaved in {path_music_dir}")
    else:
        messagebox.showerror(
            "Download failed",
            "Download failed. The video might require login.\n"
            "Please make sure one of the supported browsers (Firefox, Edge, Chrome, Opera or Brave) is installed and logged in."
        )


#--- GUI ---
root = tk.Tk()
root.title("YouTube MP3 Downloader")

tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=10, pady=10)

btn_download = tk.Button(root, text="Download MP3", command=download_mp3)
btn_download.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()