from googletrans import Translator

translator = Translator()

def translate_ja_to_en(text: str) -> str:
    return translator.translate(text, src="ja", dest="en").text
