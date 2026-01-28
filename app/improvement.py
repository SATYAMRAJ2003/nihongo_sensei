def suggest_improvements(sentence: str, grammar_level: str):
    suggestions = []

    # N4 → N3 naturalization
    if grammar_level in ["N4", "N5"]:
        suggestions.append({
            "level": "N3",
            "sentence": sentence.replace("私は", ""),
            "reason": "主語を省略するとより自然な日本語になります。"
        })

    # Politeness enhancement
    if "です" not in sentence:
        suggestions.append({
            "level": "N3",
            "sentence": sentence + "。",
            "reason": "文末を整えると丁寧な印象になります。"
        })

    return suggestions
