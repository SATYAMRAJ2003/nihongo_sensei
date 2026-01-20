# backend/app/stt.py
import os
import whisper
import torch
from googletrans import Translator
import pyttsx3

# Detect device (GPU if available, else CPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper Large once at startup
MODEL = whisper.load_model("small", device=DEVICE)

def transcribe_audio(audio_path: str) -> str:
    """Transcribes Japanese audio using Whisper Large."""
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    result = MODEL.transcribe(
        audio_path,
        language="ja",
        fp16=(DEVICE == "cuda")  # fp16 only on GPU
    )
    return result["text"]

def speak_text(text: str, lang: str = "en"):
    """Speaks text aloud. Uses English voices by default, Japanese if installed."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    if lang == "en":
        for v in voices:
            if "Zira" in v.name:
                engine.setProperty("voice", v.id)
                break
        else:
            for v in voices:
                if "David" in v.name:
                    engine.setProperty("voice", v.id)
                    break
    elif lang == "ja":
        for v in voices:
            if "Japanese" in v.name:
                engine.setProperty("voice", v.id)
                break

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    audio_file = r"D:\nihongo-sensei\data\audio_samples\sample_ja.aac"

    # Step 1: Transcribe Japanese
    ja_text = transcribe_audio(audio_file)
    print("Japanese Transcription:", ja_text)

    # Step 2: Translate into English
    translator = Translator()
    en_text = translator.translate(ja_text, src="ja", dest="en").text
    print("English Translation:", en_text)

    # Step 3: Speak both outputs
    speak_text(ja_text, lang="ja")
    speak_text(en_text, lang="en")