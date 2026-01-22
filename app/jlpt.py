def jlpt_feedback_level(score: float) -> str:
    if score >= 90:
        return "N3"
    elif score >= 75:
        return "N4"
    elif score >= 50:
        return "N5"
    else:
        return "Below N5"
