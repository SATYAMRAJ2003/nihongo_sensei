def local_sensei_feedback(
    japanese: str,
    english: str,
    pronunciation_score: float,
    jlpt_level: str
) -> str:
    feedback = []

    # Pronunciation feedback
    if pronunciation_score >= 90:
        feedback.append("素晴らしい発音です！とても自然です。")
    elif pronunciation_score >= 75:
        feedback.append("いい発音ですね。もう少し練習すると完璧です。")
    elif pronunciation_score >= 50:
        feedback.append("発音は分かりますが、ゆっくり話すと良くなります。")
    else:
        feedback.append("発音が少し難しいようです。基本音から練習しましょう。")

    # JLPT guidance
    if jlpt_level == "N5":
        feedback.append("N5レベルです。短い文と基本単語を練習しましょう。")
    elif jlpt_level == "N4":
        feedback.append("N4レベルです。助詞と動詞の形に注意しましょう。")
    elif jlpt_level == "N3":
        feedback.append("N3レベルです。自然な表現に挑戦しましょう。")
    else:
        feedback.append("まずはひらがなと基本表現から始めましょう。")

    if english:
        feedback.append(f"英語の意味: {english}")

    return " ".join(feedback)
