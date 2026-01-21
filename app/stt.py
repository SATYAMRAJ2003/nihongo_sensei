import os
import whisper
import torch

# Select device automatically
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load Whisper model once at startup
MODEL = whisper.load_model("small", device=DEVICE)


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes Japanese speech audio into text using Whisper.

    Args:
        audio_path (str): Path to the audio file

    Returns:
        str: Transcribed Japanese text
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")

    result = MODEL.transcribe(
        audio_path,
        language="ja",
        fp16=(DEVICE == "cuda")
    )

    return result["text"]
