import os
import whisper
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = whisper.load_model("small", device=DEVICE)

def transcribe_audio(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"File not found: {audio_path}")

    result = MODEL.transcribe(
        audio_path,
        language="ja",
        fp16=(DEVICE == "cuda")
    )

    return result["text"].strip()
