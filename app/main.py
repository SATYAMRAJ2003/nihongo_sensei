from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.stt import transcribe_audio
from googletrans import Translator

app = FastAPI()
translator = Translator()

# ✅ Add this root route
@app.get("/")
def root():
    return {"message": "Nihongo-Sensei backend is running!"}

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Step 1: Transcribe Japanese
        ja_text = transcribe_audio(file_path)

        # Step 2: Translate into English
        en_text = translator.translate(ja_text, src="ja", dest="en").text
    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)

    return {
        "japanese": ja_text,
        "english": en_text
    }