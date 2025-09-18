import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
import yt_dlp

# --- Script directory ---
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Music directory under the script folder ---
path_music_dir = os.path.join(script_dir, "music")
os.makedirs(path_music_dir, exist_ok=True)

# --- Path to cookies file (exported from your browser (firefox tool)) ---
cookies_file = os.path.join(script_dir, "cookies.txt")

# --- Function to clean filenames ---
def clean_filename(name, ext):
    invalid_chars = r'\/:*?"<>|'
    for c in invalid_chars:
        name = name.replace(c, "_")
    if not name.lower().endswith(ext):
        name += ext
    return name

# --- Generic download function using cookies if available ---
def download_file(url, filename, format_type="mp3"):
    # Full absolute path to save file
    out_path = os.path.join(path_music_dir, filename)
    # Ensure directory exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    success = False

    # Build command for mp3 or mp4
    if format_type == "mp3":
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3", "-o", out_path, "--newline", url]
    else:  # mp4
        cmd = [
            "yt-dlp",
            "-f", "bestvideo+bestaudio/best",
            "-o", out_path,
            "--merge-output-format", "mp4",
            "--newline",
            url
        ]

    # Add cookies if file exists
    if os.path.exists(cookies_file):
        cmd += ["--cookies", cookies_file]

    print("Downloading to:", out_path)  # Debug: show full path

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
        else:
            progress_label.config(text="Download failed. Check URL or cookies if needed.")
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
        messagebox.showerror("Download failed", "Download failed. Check URL or cookies if needed.")

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
        messagebox.showerror("Download failed", "Download failed. Check URL or cookies if needed.")

# --- GUI ---
root = tk.Tk()
root.title("Universal Audio/Video Downloader (Linux)")

tk.Label(root, text="Video/Audio URL:").grid(row=0, column=0, padx=10, pady=10)
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=10, pady=10)

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
