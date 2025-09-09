import streamlit as st
import PyPDF2
import pyttsx3
from pydub import AudioSegment
import os
import nltk

# Download NLTK tokenizer
nltk.download('punkt', quiet=True)

# 🎭 Emotion → Music mapping
emotion_dict = {
    "happy": "happy.mp3",
    "joy": "happy.mp3",
    "excited": "happy.mp3",
    "angry": "angry.mp3",
    "mad": "angry.mp3",
    "sad": "sad.mp3",
    "cry": "sad.mp3",
    "fear": "scary.mp3",
    "scared": "scary.mp3",
    "surprise": "calm.mp3",
    "calm": "calm.mp3",
    "relaxed": "calm.mp3"
}

def detect_emotion(text):
    text = text.lower()
    for word, music in emotion_dict.items():
        if word in text:
            return word, music
    return "neutral", "calm.mp3"

def pdf_to_emotional_audio(pdf_file):
    # Extract text
    reader = PyPDF2.PdfReader(pdf_file)
    text_content = ""
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            text_content += txt + "\n"

    if text_content.strip() == "":
        st.warning("⚠️ No text found in PDF")
        return None

    # Detect emotion
    emotion, music_file = detect_emotion(text_content[:500])
    st.success(f"🎭 Detected Emotion: {emotion}")

    # Convert PDF to voice
    speaker = pyttsx3.init()
    voice_output = "temp_voice.wav"
    speaker.save_to_file(text_content, voice_output)
    speaker.runAndWait()

    # Mix background music
    try:
        if os.path.exists(music_file):
            voice = AudioSegment.from_file(voice_output)
            music = AudioSegment.from_file(music_file) - 15  # lower music volume

            if len(music) < len(voice):
                times = (len(voice) // len(music)) + 1
                music = music * times

            final_audio = music.overlay(voice)
            output_file = "final_audio.mp3"
            final_audio.export(output_file, format="mp3")
        else:
            st.warning(f"⚠️ Background music not found: {music_file}. Only voice saved.")
            output_file = "final_audio.wav"
            os.rename(voice_output, output_file)

        return output_file

    except Exception as e:
        st.warning("⚠️ FFmpeg missing or failed, saving voice-only audio instead.")
        output_file = "final_audio.wav"
        os.rename(voice_output, output_file)
        return output_file

# --- Streamlit UI ---
st.set_page_config(page_title="EchoVerse", layout="centered")
st.title("🎵 EchoVerse - PDF to Emotional Audio")
st.write("Upload a PDF, detect emotion, convert to speech, and download with matching background music!")

uploaded_file = st.file_uploader("📂 Upload PDF", type=["pdf"])

if uploaded_file:
    if st.button("🎶 Generate Audio"):
        with st.spinner("Processing PDF..."):
            audio_file = pdf_to_emotional_audio(uploaded_file)
            if audio_file:
                st.success("✅ Audio Generated!")
                st.audio(audio_file, format='audio/mp3')
                st.download_button(
                    label="⬇️ Download Audio",
                    data=open(audio_file, "rb").read(),
                    file_name=audio_file,
                    mime="audio/mp3"
                )
