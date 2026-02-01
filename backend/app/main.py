from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

from app.improvement import suggest_improvements
from app.stt import transcribe_audio
from app.translate import translate_ja_to_en
from app.pronunciation import pronunciation_score, pronunciation_feedback
from app.jlpt import jlpt_feedback_level
from app.local_sensei import local_sensei_feedback
from app.grammar import (
    detect_grammar_patterns,
    detect_grammar_mistakes,
    grammar_jlpt_level,
    grammar_feedback,
    suggest_grammar_corrections
)
from app.session_store import create_session, update_session, get_session
from app.recommendation import generate_practice_recommendations
from app.progression import determine_next_difficulty
from app.weak_area import detect_weak_area
from app.roadmap import generate_learning_roadmap


app = FastAPI(title="Nihongo Sensei API")

# ✅ CORS (safe for frontend deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Nihongo Sensei backend running"}


@app.post("/speech-to-text")
async def speech_to_text(
    file: UploadFile = File(...),
    expected_text: str = Form(...),
    session_id: str = Form(None)
):
    # ✅ Validate file type
    if file.content_type not in ["audio/wav", "audio/mpeg", "audio/aac"]:
        return {"error": "Unsupported audio format"}

    # ✅ Safe temp file
    temp_path = f"temp_{uuid.uuid4()}.wav"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 0️⃣ Session handling
        if not session_id:
            session_id = create_session()

        previous_session = get_session(session_id)
        previous_score = (
            previous_session.get("last_pronunciation")
            if previous_session else None
        )

        # 1️⃣ Speech → Text
        japanese_text = transcribe_audio(temp_path)

        # 2️⃣ Translation
        english_text = translate_ja_to_en(japanese_text)

        # 3️⃣ Pronunciation
        expected_text = expected_text.strip()
        score = pronunciation_score(expected_text, japanese_text)
        pronunciation_feedback_text = pronunciation_feedback(score)
        pronunciation_jlpt = jlpt_feedback_level(score)

        # 🔁 Progression logic
        progression = determine_next_difficulty(
            previous_score=previous_score,
            current_score=score,
            current_level=pronunciation_jlpt
        )

        if previous_score is None:
            progress_feedback = "First attempt recorded."
        elif score > previous_score:
            progress_feedback = "Great! Your pronunciation improved 👍"
        elif score < previous_score:
            progress_feedback = "Your score dropped slightly. Try speaking slower."
        else:
            progress_feedback = "Your pronunciation is consistent."

        # 4️⃣ Grammar analysis
        grammar_patterns = detect_grammar_patterns(japanese_text)
        grammar_mistakes = detect_grammar_mistakes(japanese_text)
        grammar_level = grammar_jlpt_level(grammar_patterns)

        grammar_feedback_text = grammar_feedback(
            grammar_patterns,
            grammar_level
        )

        grammar_corrections = (
            suggest_grammar_corrections(japanese_text)
            if grammar_mistakes else []
        )

        # 5️⃣ Sentence improvements
        improvements = suggest_improvements(
            japanese_text,
            grammar_level
        )

        # 6️⃣ Sensei feedback
        sensei_reply = local_sensei_feedback(
            japanese=japanese_text,
            english=english_text,
            pronunciation_score=score,
            jlpt_level=pronunciation_jlpt
        )

        # 7️⃣ Weak areas + recommendations
        weak_area_analysis = detect_weak_area(
            pronunciation_score=score,
            grammar_level=grammar_level
        )

        practice_recommendations = generate_practice_recommendations(
            weak_area=weak_area_analysis["weak_area"],
            grammar_level=grammar_level
        )

        learning_roadmap = generate_learning_roadmap(
            current_level=progression["next_level"],
            weak_area=weak_area_analysis["weak_area"],
            grammar_level=grammar_level
        )

        # 8️⃣ Update session
        update_session(session_id, {
            "last_sentence": japanese_text,
            "last_pronunciation": score,
            "last_grammar_level": grammar_level,
            "current_level": progression["next_level"]
        })

    except Exception as e:
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "session_id": session_id,

        "japanese": japanese_text,
        "english": english_text,
        "expected": expected_text,

        "pronunciation_score": score,
        "pronunciation_feedback": pronunciation_feedback_text,
        "pronunciation_jlpt": pronunciation_jlpt,
        "progress_feedback": progress_feedback,

        "grammar_patterns": grammar_patterns,
        "grammar_jlpt": grammar_level,
        "grammar_feedback": grammar_feedback_text,
        "grammar_mistakes": grammar_mistakes,
        "grammar_corrections": grammar_corrections,

        "weak_area": weak_area_analysis,
        "practice_recommendations": practice_recommendations,

        "improved_sentences": improvements,
        "sensei_reply": sensei_reply,
        "learning_roadmap": learning_roadmap
    }
