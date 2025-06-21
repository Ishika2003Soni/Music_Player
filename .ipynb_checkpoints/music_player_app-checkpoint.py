import streamlit as st
import os
import subprocess
from pathlib import Path
from pydub import AudioSegment
import random
from datetime import datetime
from tkinter import Tk, filedialog
import speech_recognition as sr

# ------------------ Configurations ------------------
st.set_page_config(page_title="🎵 Smart Music Player", layout="centered")
songs_dir = "songs"
covers_dir = "covers"
playlists_dir = "playlists"
favorites_file = "favorites.txt"

# Create folders if not exist
os.makedirs(songs_dir, exist_ok=True)
os.makedirs(covers_dir, exist_ok=True)
os.makedirs(playlists_dir, exist_ok=True)
if not os.path.exists(favorites_file):
    open(favorites_file, "a").close()

# ------------------ Sidebar ------------------
st.sidebar.title("🎶 Options")

if st.sidebar.button("📂 Auto-Import from Folder"):
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory()
    if folder:
        for file in os.listdir(folder):
            if file.endswith(".mp3"):
                src = os.path.join(folder, file)
                dst = os.path.join(songs_dir, file)
                if not os.path.exists(dst):
                    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                        fdst.write(fsrc.read())
        st.sidebar.success("Songs imported successfully!")

uploaded_file = st.sidebar.file_uploader("Upload MP3", type=["mp3"])
if uploaded_file:
    with open(os.path.join(songs_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.read())
    st.sidebar.success("Uploaded successfully!")

# ------------------ Favorites ------------------
with open(favorites_file, "r") as f:
    favorites = f.read().splitlines()

# ------------------ Search Input or Voice ------------------
st.title("🎵 Smart Music Player")

col1, col2 = st.columns([3, 1])
query = col1.text_input("🔍 Enter or Speak a Song Name")

if col2.button("🎙️ Speak"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... please speak your song name")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            st.success(f"You said: **{query}**")
        except Exception as e:
            st.error(f"❌ Could not recognize speech: {e}")
            query = ""

# ------------------ Smart Download ------------------
def search_and_download(song_name):
    st.info(f"🔍 Downloading: {song_name}")
    try:
        cmd = ["yt-dlp", "-x", "--audio-format", "mp3",
               "-o", f"{songs_dir}/%(title)s.%(ext)s",
               f"ytsearch1:{song_name}"]
        subprocess.run(cmd, check=True)
        st.success("✅ Song downloaded successfully!")
    except Exception as e:
        st.error(f"❌ Download failed: {e}")

# ------------------ Load Songs ------------------
songs = sorted([f for f in os.listdir(songs_dir) if f.endswith(".mp3")])

if query:
    matched = [s for s in songs if query.lower() in s.lower()]
    if not matched:
        search_and_download(query)
        songs = sorted([f for f in os.listdir(songs_dir) if f.endswith(".mp3")])
        matched = [s for s in songs if query.lower() in s.lower()]
else:
    matched = songs

# ------------------ UI ------------------
if matched:
    selected = st.selectbox("🎧 Choose Song", matched)
    song_path = os.path.join(songs_dir, selected)
    st.audio(song_path, format="audio/mp3")

    try:
        audio = AudioSegment.from_file(song_path)
        duration = int(audio.duration_seconds)
        st.info(f"⏱️ Duration: {duration // 60}:{duration % 60:02d} min")
    except:
        st.warning("⚠️ Duration could not be read.")

    # Favorites
    is_fav = selected in favorites
    if st.button("💔 Remove from Favorites" if is_fav else "❤️ Add to Favorites"):
        if is_fav:
            favorites.remove(selected)
        else:
            favorites.append(selected)
        with open(favorites_file, "w") as f:
            f.write("\n".join(favorites))
        st.success("Favorites updated!")
        st.rerun()

    # Download / Delete
    col3, col4 = st.columns(2)
    with col3:
        with open(song_path, "rb") as f:
            st.download_button("⬇️ Download", f, file_name=selected)
    with col4:
        if st.button("🗑️ Delete Song"):
            os.remove(song_path)
            st.success("Deleted.")
            st.rerun()

# ------------------ View All Songs ------------------
with st.expander("📃 View All Songs"):
    for s in songs:
        time_str = datetime.fromtimestamp(os.path.getmtime(os.path.join(songs_dir, s))).strftime("%d %b %Y")
        heart = "❤️" if s in favorites else ""
        st.markdown(f"🎵 `{s}` {heart} *({time_str})*")

# ------------------ Footer ------------------
st.markdown("""
---
**ℹ️ Features:**
- 🎙️ Voice & text-based search
- 🔍 Smart YouTube audio search and download
- 📤 Upload or import songs
- 🎧 Stream songs, add to favorites, delete or download
""")
