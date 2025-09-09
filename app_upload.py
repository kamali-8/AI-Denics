import streamlit as st
from PyPDF2 import PdfReader
import pyttsx3
import tempfile
import os

st.title("📚 EchoVerse AI – PDF to Audiobook (Offline)")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Read PDF
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "

    st.subheader("📖 Extracted Text")
    st.write(text[:1000] + "...")  # preview first 1000 chars

    # Convert to speech
    if st.button("🎧 Convert to Audiobook"):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)  # speed
        engine.setProperty("volume", 1)  # volume

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            audio_path = tmp_file.name

        # Save as audio file
        engine.save_to_file(text, audio_path)
        engine.runAndWait()

        st.success("✅ Audiobook generated!")
        st.audio(audio_path, format="audio/mp3")
