from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.stt import transcribe_audio
from app.translate import translate_ja_to_en

app = FastAPI(title="Nihongo Sensei API")


# Enable CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Nihongo-Sensei backend running"}


@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    """
    Accepts an audio file, converts Japanese speech to text,
    then translates it into English.
    """
    temp_path = f"temp_{file.filename}"

    # Save uploaded file temporarily
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        japanese_text = transcribe_audio(temp_path)
        english_text = translate_ja_to_en(japanese_text)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "japanese": japanese_text,
        "english": english_text
    }
