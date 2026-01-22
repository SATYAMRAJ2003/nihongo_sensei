from deep_translator import GoogleTranslator

def translate_ja_to_en(ja_text: str) -> str:
    if not ja_text.strip():
        return ""

    translator = GoogleTranslator(source="ja", target="en")
    return translator.translate(ja_text)
