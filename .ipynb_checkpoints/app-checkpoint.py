import streamlit as st
import os
import subprocess
from pydub import AudioSegment
from pathlib import Path
from PIL import Image
import speech_recognition as sr

# ------------ Config ------------
st.set_page_config(page_title="🎵 Smart Music Player", layout="centered")
songs_dir = "songs"
covers_dir = "covers"
os.makedirs(songs_dir, exist_ok=True)
os.makedirs(covers_dir, exist_ok=True)

# ------------ Upload MP3 ------------
st.sidebar.header("📄 Upload MP3")
uploaded = st.sidebar.file_uploader("Upload", type=["mp3"])
if uploaded:
    with open(os.path.join(songs_dir, uploaded.name), "wb") as f:
        f.write(uploaded.read())
    st.sidebar.success("Uploaded!")

# ------------ Voice Input ------------
st.sidebar.subheader("🎙️ Voice Search")
query = ""
if st.sidebar.button("🎧 Speak Song Name"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            st.success(f"You said: {query}")
        except:
            st.error("Could not recognize speech.")
else:
    query = st.text_input("🔎 Search or Enter Song Name")

# ------------ Smart Download ------------
def search_and_download(song_name):
    st.info(f"🔍 Searching: {song_name}")
    try:
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3",
            "-o", f"{songs_dir}/%(title)s.%(ext)s",
            f"ytsearch1:{song_name}"
        ], check=True)
        st.success("✅ Downloaded!")
        # Thumbnail download
        subprocess.run([
            "yt-dlp", "--write-thumbnail", "--skip-download",
            "-o", f"{covers_dir}/%(title)s.%(ext)s",
            f"ytsearch1:{song_name}"
        ])
    except Exception as e:
        st.error(f"❌ Failed: {e}")

# ------------ Song List ------------
songs = sorted([f for f in os.listdir(songs_dir) if f.endswith(".mp3")])
matched = [s for s in songs if query.lower() in s.lower()] if query else songs

if query and not matched:
    search_and_download(query)
    songs = sorted([f for f in os.listdir(songs_dir) if f.endswith(".mp3")])
    matched = [s for s in songs if query.lower() in s.lower()]

if matched:
    selected = st.selectbox("🎼 Choose Song", matched)
    st.audio(os.path.join(songs_dir, selected), format="audio/mp3")

    try:
        audio = AudioSegment.from_file(os.path.join(songs_dir, selected))
        m, s = divmod(int(audio.duration_seconds), 60)
        st.info(f"⏱️ Duration: {m}:{s:02d}")
    except:
        st.warning("Couldn't read duration.")

    # Thumbnail
    thumb_path = os.path.join(covers_dir, f"{Path(selected).stem}.webp")
    if os.path.exists(thumb_path):
        st.image(thumb_path, width=300, caption="Album Art")

# ------------ View All Songs ------------
with st.expander("📂 All Songs"):
    for s in songs:
        st.markdown(f"🎶 `{s}`")

# ------------ Footer ------------
with st.expander("ℹ️ About App"):
    st.markdown("""
    - 🔍 Smart Search & Auto-download songs (audio only)
    - 🎙️ Voice search supported
    - 🖼️ YouTube thumbnail as album art
    - 🎧 Audio playback and MP3 upload
    """)