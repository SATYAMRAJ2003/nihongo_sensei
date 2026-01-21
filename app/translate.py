from deep_translator import GoogleTranslator


def translate_ja_to_en(ja_text: str) -> str:
    """
    Translates Japanese text to English.

    Args:
        ja_text (str): Japanese text

    Returns:
        str: English translation
    """
    if not ja_text.strip():
        return ""

    translator = GoogleTranslator(source="ja", target="en")
    return translator.translate(ja_text)
