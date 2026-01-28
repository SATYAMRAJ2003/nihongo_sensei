def generate_learning_roadmap(
    current_level: str,
    weak_area: str,
    grammar_level: str
):
    roadmap = {
        "current_level": current_level,
        "next_target": None,
        "focus_areas": [],
        "daily_plan": [],
        "example_practice": []
    }

    # 🎯 Decide next JLPT target
    jlpt_order = ["N5", "N4", "N3", "N2", "N1"]
    if current_level in jlpt_order:
        idx = jlpt_order.index(current_level)
        roadmap["next_target"] = (
            jlpt_order[idx + 1] if idx < len(jlpt_order) - 1 else "N1"
        )

    # 🧠 Weak area based focus
    if weak_area == "pronunciation":
        roadmap["focus_areas"] = [
            "Pitch accent",
            "Long vowels",
            "Clear consonants"
        ]
        roadmap["daily_plan"] = [
            "Shadow native audio (10 min)",
            "Repeat sentences slowly",
            "Record and compare pronunciation"
        ]
        roadmap["example_practice"] = [
            "私は毎日日本語を勉強しています。",
            "昨日友達と映画を見ました。"
        ]

    elif weak_area == "grammar":
        roadmap["focus_areas"] = [
            "Particle usage",
            "Verb conjugation",
            "Sentence structure"
        ]
        roadmap["daily_plan"] = [
            "Study 2 grammar patterns",
            "Create 3 original sentences",
            "Speak them aloud"
        ]
        roadmap["example_practice"] = [
            "学校に行かなければなりません。",
            "日本語を話すことが好きです。"
        ]

    else:  # both
        roadmap["focus_areas"] = [
            "Grammar accuracy",
            "Pronunciation clarity"
        ]
        roadmap["daily_plan"] = [
            "Grammar drill (10 min)",
            "Pronunciation shadowing (10 min)",
            "Free speaking practice"
        ]
        roadmap["example_practice"] = [
            "将来日本で働きたいです。",
            "毎朝ニュースを聞いています。"
        ]

    return roadmap
