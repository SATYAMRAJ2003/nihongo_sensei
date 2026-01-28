def determine_next_difficulty(
    previous_score: float,
    current_score: float,
    current_level: str
):
    # Default: stay same
    next_level = current_level
    message = "Keep practicing at the same level."

    # Improvement
    if previous_score is not None:
        if current_score - previous_score >= 10:
            if current_level == "Below N5":
                next_level = "N5"
            elif current_level == "N5":
                next_level = "N4"
            elif current_level == "N4":
                next_level = "N3"

            message = "Great improvement! Difficulty increased."

        # Decline
        elif previous_score - current_score >= 10:
            message = "Let's slow down and strengthen basics."

    return {
        "next_level": next_level,
        "progression_message": message
    }
