def detect_weak_area(pronunciation_score: float, grammar_level: str) -> dict:
    """
    Detects learner weak area based on pronunciation & grammar.
    """

    grammar_rank = {
        "Below N5": 0,
        "N5": 1,
        "N4": 2,
        "N3": 3,
        "N2": 4,
        "N1": 5
    }

    weak_areas = []

    if pronunciation_score < 70:
        weak_areas.append("pronunciation")

    if grammar_rank.get(grammar_level, 0) < 2:
        weak_areas.append("grammar")

    if not weak_areas:
        return {
            "weak_area": "balanced",
            "message": "Great balance between pronunciation and grammar. Keep practicing!"
        }

    return {
        "weak_area": weak_areas,
        "message": f"You should focus more on {', '.join(weak_areas)}."
    }
