from langdetect import detect
from deep_translator import GoogleTranslator

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"

def translate_to_english(text: str, source_lang: str) -> str:
    if source_lang == "en":
        return text
    try:
        return GoogleTranslator(source=source_lang, target="en").translate(text)
    except Exception:
        return text

def translate_from_english(text: str, target_lang: str) -> str:
    if target_lang == "en":
        return text
    try:
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception:
        return text