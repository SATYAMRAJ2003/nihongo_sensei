from difflib import SequenceMatcher

def pronunciation_score(expected: str, spoken: str) -> float:
    if not expected or not spoken:
        return 0.0

    if expected not in spoken:
        return 0.0

    similarity = SequenceMatcher(None, expected, spoken).ratio()
    return round(similarity * 100, 2)
def pronunciation_feedback(score: float) -> str:
    if score == 0:
        return "You spoke a different sentence. Try saying the expected phrase clearly."
    elif score >= 90:
        return "Excellent pronunciation! とても上手です 🎉"
    elif score >= 75:
        return "Good pronunciation, but a few sounds need practice."
    elif score >= 50:
        return "Your pronunciation needs improvement. Try speaking slowly."
    else:
        return "Pronunciation is unclear. Focus on basic Japanese sounds."
