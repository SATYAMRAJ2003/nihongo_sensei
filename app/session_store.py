import uuid

# Simple in-memory session store
SESSION_STORE = {}

def create_session():
    session_id = str(uuid.uuid4())
    SESSION_STORE[session_id] = {
        "history": [],
        "last_pronunciation": None,
        "last_grammar": None
    }
    return session_id

def update_session(session_id, data):
    if session_id in SESSION_STORE:
        SESSION_STORE[session_id]["history"].append(data)
        SESSION_STORE[session_id]["last_pronunciation"] = data.get("pronunciation_score")
        SESSION_STORE[session_id]["last_grammar"] = data.get("grammar_jlpt")

def get_session(session_id):
    return SESSION_STORE.get(session_id)
