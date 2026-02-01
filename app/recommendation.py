def generate_practice_recommendations(
    weak_area,
    grammar_level: str
):
    recommendations = []

    # Pronunciation focus
    if "pronunciation" in weak_area:
        recommendations.extend([
            "Repeat basic greetings aloud (こんにちは, おはようございます)",
            "Practice mora timing using slow speech",
            "Shadow native Japanese audio for 5 minutes"
        ])

    # Grammar focus
    if "grammar" in weak_area:
        if grammar_level in ["Below N5", "N5"]:
            recommendations.extend([
                "Practice は and を particles",
                "Create 5 sentences using ます form",
                "Translate simple English sentences to Japanese"
            ])
        elif grammar_level == "N4":
            recommendations.extend([
                "Practice ています form",
                "Use past tense sentences",
                "Write a short daily routine paragraph"
            ])

    # Balanced learner
    if weak_area == "balanced":
        recommendations.extend([
            "Practice speaking full sentences",
            "Try explaining your day in Japanese",
            "Shadow intermediate-level dialogues"
        ])

    return recommendations
