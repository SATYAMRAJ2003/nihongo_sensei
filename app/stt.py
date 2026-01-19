import os
import whisper
from googletrans import Translator
import pyttsx3

def transcribe_audio(audio_path: str):
    """Transcribes Japanese audio using Whisper."""
    if r"C:\ffmpeg\bin" not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="ja", task="transcribe")
    return result["text"]

def speak_text(text: str, lang: str = "en"):
    """Speaks text aloud. Uses English voices by default, Japanese if installed."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    if lang == "en":
        # Prefer Zira, fallback to David
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
        # Will only work once you install a Japanese voice in Windows
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