# MP3 & MP4 Downloader (Python)

A simple and lightweight Python GUI tool to download online videos as **MP3** or **MP4** files on Windows.  
It automatically handles dependencies like **ffmpeg** and uses **yt-dlp** for extraction.  
Designed for private, legal use only. 

## Features
- GUI built with **Tkinter**
- Automatically downloads **ffmpeg** if missing
- Automatically downloads **yt-dlp** if missing 
- Supports MP3 and MP4 output
- Uses browser cookies (Firefox, Edge, Chrome, Opera, Brave) if login is required
- Saves files into a local `music` directory
- Tested with **Python 3.13.7**

---

## Usage Disclaimer
This tool is intended for **private, legal use only**.  
Downloading copyrighted content without permission may violate the Terms of Service of certain platforms.  
Only download content you own or that is licensed for free use.  

---

## Installation & Usage

### Step 1: Install Python
- Download Python from [python.org](https://www.python.org/)  
- During installation, make sure to check **Add Python to PATH**

### Step 2: Verify Pip
Press: __Win + R__

Type: __cmd__
and click __OK__ to execute it. 
 
Execute in cmd: pip --version

If you see a version number it is already installed and go to the next step.

Usually it is already installed with Python V 3.4 or higher.

__If not__:
  Get the code (https://bootstrap.pypa.io/get-pip.py) and save it as get-pip.py.
  Open a cmd in the same dir as get-pip.py and execute: 
  
  python get-pip.py
  
  Test again by excecute: pip --version
### Step 3: Run the Downloader
1. Download the __Python_Youtube_MP3_Downloader_Win.pyw__ file.
2. Run the file and wait; it will automatically download ffmpeg and yt-dlp if missing.
4. Enter a video/audio URL in the GUI
5. Choose a Save name.
6. Click __Download MP3__ or __Download MP4__.
7. Files will be saved in the local music directory (auto-created if missing).

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.




