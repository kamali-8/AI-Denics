import PyPDF2
import pyttsx3
import os
import nltk
from tkinter import Tk, filedialog

# Download NLTK tokenizer once
nltk.download('punkt', quiet=True)

# Simple emotion → music mapping
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
    return "neutral", None  # no music if neutral

def pdf_to_audio():
    # Choose PDF
    Tk().withdraw()
    pdf_file = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF Files","*.pdf")])
    if not pdf_file:
        print("❌ No PDF selected")
        return

    # Extract text
    reader = PyPDF2.PdfReader(pdf_file)
    text_content = ""
    for page in reader.pages:
        txt = page.extract_text()
        if txt:
            text_content += txt + "\n"

    if text_content.strip() == "":
        print("⚠️ No text found in PDF")
        return

    # Detect emotion
    emotion, music_file = detect_emotion(text_content[:500])
    print(f"🎭 Detected Emotion: {emotion}")

    # Convert to speech
    speaker = pyttsx3.init()
    voice_file = "temp_voice.wav"
    speaker.save_to_file(text_content, voice_file)
    speaker.runAndWait()

    # Mix background music if possible
    try:
        if music_file and os.path.exists(music_file):
            from pydub import AudioSegment
            voice = AudioSegment.from_file(voice_file)
            music = AudioSegment.from_file(music_file) - 15

            if len(music) < len(voice):
                times = (len(voice) // len(music)) + 1
                music = music * times

            final_audio = music.overlay(voice)
            output_file = os.path.splitext(pdf_file)[0] + "_final.mp3"
            final_audio.export(output_file, format="mp3")
            print(f"✅ Final emotional audio saved: {output_file}")
        else:
            output_file = os.path.splitext(pdf_file)[0] + "_voice.wav"
            os.rename(voice_file, output_file)
            print(f"✅ Voice-only audio saved: {output_file}")
    except Exception:
        output_file = os.path.splitext(pdf_file)[0] + "_voice.wav"
        os.rename(voice_file, output_file)
        print(f"⚠️ FFmpeg/pydub missing. Voice-only audio saved: {output_file}")

if __name__ == "__main__":
    pdf_to_audio()
