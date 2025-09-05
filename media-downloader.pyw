import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox

# --- Music directory ---
path_music_dir = os.path.join(os.getcwd(), "music")
os.makedirs(path_music_dir, exist_ok=True)

# --- yt-dlp installation ---
try:
    import yt_dlp
except ImportError:
    print("yt-dlp not found. Installing it...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

# --- Download ffmpeg if not present ---
ffmpeg_path = os.path.join(os.environ['USERPROFILE'], "ffmpeg")
os.makedirs(ffmpeg_path, exist_ok=True)
bin_path = os.path.join(ffmpeg_path, "bin")

ffmpeg_exe = os.path.join(bin_path, "ffmpeg.exe")
ffprobe_exe = os.path.join(bin_path, "ffprobe.exe")
ffplay_exe = os.path.join(bin_path, "ffplay.exe")

if not (os.path.isfile(ffmpeg_exe) and os.path.isfile(ffprobe_exe) and os.path.isfile(ffplay_exe)):
    print("ffmpeg not found. Downloading...")
    zip_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_file = os.path.join(ffmpeg_path, "ffmpeg.zip")

    urllib.request.urlretrieve(zip_url, zip_file)
    print("Download complete. Extracting...")

    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(ffmpeg_path)

    extracted_folder = None
    for f in os.listdir(ffmpeg_path):
        full_path = os.path.join(ffmpeg_path, f)
        if os.path.isdir(full_path) and f.startswith("ffmpeg"):
            extracted_folder = full_path
            break

    if extracted_folder is None:
        raise Exception("Extracted ffmpeg folder not found!")

    extracted_bin = os.path.join(extracted_folder, "bin")
    os.makedirs(bin_path, exist_ok=True)
    for file in os.listdir(extracted_bin):
        shutil.move(os.path.join(extracted_bin, file), os.path.join(bin_path, file))

    os.remove(zip_file)
    shutil.rmtree(extracted_folder)
    print("ffmpeg setup complete.")

# --- Function to update title in Save-as field for YouTube URLs ---
def update_title(*args):
    url = entry_url.get().strip()
    if "youtube.com" in url or "youtu.be" in url:
        try:
            ydl_opts = {"quiet": True, "no_warnings": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get("title", "")
                if title:
                    entry_name.delete(0, tk.END)
                    entry_name.insert(0, title)
        except Exception:
            pass  # fail silently

# --- Function to clean filenames ---
def clean_filename(name, ext):
    invalid_chars = r'\/:*?"<>|'
    for c in invalid_chars:
        name = name.replace(c, "_")
    if not name.lower().endswith(ext):
        name += ext
    return name

# --- Generic download function with GUI progress ---
def download_file(url, filename, format_type="mp3"):
    out_path = os.path.join(path_music_dir, filename)
    success = False

    if format_type == "mp3":
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "--ffmpeg-location", bin_path, "-o", out_path, "--newline", url]
    else:  # mp4
        cmd = ["yt-dlp", "-f", "best", "-o", out_path, "--newline", url]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            line = line.strip()
            if "%" in line:
                try:
                    perc = line.split("%")[0].split()[-1]
                    progress_label.config(text=f"Progress: {perc}%")
                    root.update_idletasks()
                except:
                    pass
        process.wait()
        if process.returncode == 0:
            success = True
            progress_label.config(text="Progress: 100% - Complete!")
    except subprocess.CalledProcessError:
        pass

    return success, out_path

# --- Wrapper functions ---
def download_mp3():
    url = entry_url.get().strip()
    title = entry_name.get().strip()
    if not url or not title:
        messagebox.showwarning("Input error", "Please enter URL and filename.")
        return
    filename = clean_filename(title, ".mp3")
    success, out_path = download_file(url, filename, "mp3")
    if success:
        messagebox.showinfo("Success", f"Download complete!\nSaved as {out_path}")
    else:
        messagebox.showerror("Download failed", "Download failed. Check URL or login if needed.")

def download_mp4():
    url = entry_url.get().strip()
    title = entry_name.get().strip()
    if not url or not title:
        messagebox.showwarning("Input error", "Please enter URL and filename.")
        return
    filename = clean_filename(title, ".mp4")
    success, out_path = download_file(url, filename, "mp4")
    if success:
        messagebox.showinfo("Success", f"Download complete!\nSaved as {out_path}")
    else:
        messagebox.showerror("Download failed", "Download failed. Check URL or login if needed.")

# --- GUI ---
root = tk.Tk()
root.title("Universal Audio/Video Downloader")

tk.Label(root, text="Video/Audio URL:").grid(row=0, column=0, padx=10, pady=10)
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=10, pady=10)
entry_url.bind("<FocusOut>", update_title)

tk.Label(root, text="Save as:").grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(root, width=50)
entry_name.grid(row=1, column=1, padx=10, pady=5)

btn_download_mp3 = tk.Button(root, text="Download MP3", command=download_mp3)
btn_download_mp4 = tk.Button(root, text="Download MP4", command=download_mp4)
btn_download_mp3.grid(row=2, column=0, columnspan=2, pady=10)
btn_download_mp4.grid(row=3, column=0, columnspan=2, pady=10)

progress_label = tk.Label(root, text="Progress: 0%")
progress_label.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()
