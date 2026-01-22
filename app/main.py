from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from app.stt import transcribe_audio
from app.translate import translate_ja_to_en
from app.pronunciation import pronunciation_score, pronunciation_feedback
from app.jlpt import jlpt_feedback_level
from app.local_sensei import local_sensei_feedback

app = FastAPI(title="Nihongo Sensei API")

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
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1️⃣ Speech → Text
        japanese_text = transcribe_audio(temp_path)

        # 2️⃣ Translation
        english_text = translate_ja_to_en(japanese_text)

        # 3️⃣ Pronunciation (basic reference for now)
        basic_phrases = [
            "こんにちは",
            "ありがとうございます",
            "おはようございます"
        ]
        expected_text = basic_phrases[0]

        score = pronunciation_score(expected_text, japanese_text)
        pronunciation_feedback_text = pronunciation_feedback(score)

        # 4️⃣ JLPT estimation
        jlpt_level = jlpt_feedback_level(score)

        # 5️⃣ Local Sensei feedback (NO paid AI)
        sensei_reply = local_sensei_feedback(
            japanese=japanese_text,
            english=english_text,
            pronunciation_score=score,
            jlpt_level=jlpt_level
        )

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "japanese": japanese_text,
        "english": english_text,
        "expected": expected_text,
        "pronunciation_score": score,
        "pronunciation_feedback": pronunciation_feedback_text,
        "jlpt_level": jlpt_level,
        "sensei_reply": sensei_reply
    }
