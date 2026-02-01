# app/grammar.py

# JLPT grammar dictionary
JLPT_GRAMMAR_MAP = {
    "N5": ["は", "を", "です", "ます"],
    "N4": ["ています", "ない", "から"],
    "N3": ["ようです", "ながら"],
    "N2": ["わけではない"],
}

def detect_grammar_patterns(text: str) -> list[str]:
    patterns = []

    for level, grammar_list in JLPT_GRAMMAR_MAP.items():
        for grammar in grammar_list:
            if grammar in text:
                patterns.append(grammar)

    return list(set(patterns))


def detect_grammar_mistakes(text: str) -> list[str]:
    mistakes = []

    # Example rule: sentence without topic marker
    if "は" not in text and "が" not in text:
        mistakes.append("Missing topic marker (は / が)")

    # Example rule: polite verb missing
    if "ます" not in text and "です" not in text:
        mistakes.append("Polite verb form missing")

    return mistakes


def grammar_jlpt_level(patterns: list[str]) -> str:
    level_score = {
        "N5": 0,
        "N4": 0,
        "N3": 0,
        "N2": 0,
    }

    for pattern in patterns:
        for level, grammar_list in JLPT_GRAMMAR_MAP.items():
            if pattern in grammar_list:
                level_score[level] += 1

    # Pick highest JLPT level detected
    if level_score["N2"] > 0:
        return "N2"
    if level_score["N3"] > 0:
        return "N3"
    if level_score["N4"] > 0:
        return "N4"
    if level_score["N5"] > 0:
        return "N5"

    return "Below N5"


def grammar_feedback(patterns: list[str], level: str) -> str:
    if not patterns:
        return "基本的な文法が不足しています。N5から復習しましょう。"

    joined = "、".join(patterns)
    return f"使用されている文法: {joined}。{level}レベルです。"

def suggest_grammar_corrections(text: str):
    """
    Suggest corrected Japanese sentences for common grammar mistakes.
    Returns a list of suggestions.
    """

    suggestions = []

    # Example 1: Missing polite form
    if "勉強する" in text and "しています" not in text:
        suggestions.append({
            "mistake": "勉強する",
            "suggestion": text.replace("勉強する", "勉強しています"),
            "reason": "丁寧な現在進行形では『しています』を使います。"
        })

    # Example 2: Missing topic marker は
    if text.startswith("私") and "私は" not in text:
        suggestions.append({
            "mistake": "私",
            "suggestion": text.replace("私", "私は", 1),
            "reason": "『は』は話題を示す助詞です。"
        })

    # Example 3: Missing object marker を
    if "日本語勉強" in text:
        suggestions.append({
            "mistake": "日本語勉強",
            "suggestion": text.replace("日本語勉強", "日本語を勉強"),
            "reason": "動作の対象には助詞『を』が必要です。"
        })

    return suggestions
