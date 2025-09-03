# Free-YouTube-MP3-Downloader-Python

A simple Python GUI tool to download YouTube videos as MP3 files on Windows.  
This repository contains the Python source code only.

- GUI built with Tkinter  
- Automatically downloads ffmpeg if missing  
- Uses yt-dlp for YouTube extraction  
- Browser cookies (Firefox, Edge, Chrome, Opera, Brave) are used if login is required  
- Python version 3.13.7 was used  
- Does not include a pre-built EXE; users can create it themselves using PyInstaller  

## Usage Note
This tool is intended for private, legal use only.  
Downloading copyrighted content without permission may violate YouTube’s Terms of Service.  
Please only download videos that you own or that are licensed for free use.

## Step 1: Install Python
Install Python from [python.org](https://www.python.org/) and make sure to check __Add Python to PATH__

## Step 2: Test if Pip is installed
Press: __Win + R__

Type: __cmd__
and execute it.
 
Execute: pip --version

If you see a version number it is already installed and go to the next step.

Usually it is already installed with Python V 3.4 or higher.
__If not__:
  Get the code (https://bootstrap.pypa.io/get-pip.py) and save it as get-pip.py.
  Open a cmd in the same dir as get-pip.py and execute: 
  
  python get-pip.py
  
  Test again Excecute: pip --version
# Step 3: Download and Execute Python_Youtube_MP3_Downloader_Win.pyw 
__Run the Python_Youtube_MP3_Downloader_Win.pyw__ file and wait.  It automatically downloads ffmpeg and yt-dlp. 
Enter your YouTube link in the GUI and click "Download MP3".
# Step 4: Find your music in the music dir
Your MP3 files will be saved in the "music" directory created in the same folder as the script.

