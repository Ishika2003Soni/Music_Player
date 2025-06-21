# 🎵 Smart Music Player 🎙️

A **Streamlit-based Music Player** that allows you to:
- 🎙️ Search songs using **voice or text**
- 🔍 Automatically download and play songs from **YouTube**
- 📂 Upload or import local `.mp3` files
- 🎧 Stream and play songs with album info
- ❤️ Mark songs as favorites
- 🗑️ Delete or ⬇️ download songs
- 📃 View all added tracks

---

## 🚀 Features

- 🎤 **Voice Search**: Speak the name of the song and play it instantly  
- 🔍 **Smart Search**: Search and auto-download songs from YouTube  
- 🎵 **MP3 Upload or Folder Import**  
- 🎧 **In-App Audio Playback**  
- ⏱️ **Shows Duration** of selected song  
- ❤️ **Add/Remove Favorites**  
- ⬇️ **Download** or 🗑️ **Delete** tracks  
- 📃 **View Song Library with Dates**

---

## 📸 Screenshots

![Music Player Screenshot](screenshot.png)

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/smart-music-player.git
cd smart-music-player

### 2. Create a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On macOS/Linux

###3. Install dependencies
pip install -r requirements.txt

⚙️ Additional Setup
1. Install FFmpeg
Required for audio conversion by pydub and yt-dlp.
Windows:
Download from: https://ffmpeg.org/download.html
Extract and add /bin folder to your system PATH
Linux/macOS:
sudo apt install ffmpeg        # Debian/Ubuntu
brew install ffmpeg            # macOS (via Homebrew)

2. Install PyAudio (for voice input)
pip install pipwin
pipwin install pyaudio
