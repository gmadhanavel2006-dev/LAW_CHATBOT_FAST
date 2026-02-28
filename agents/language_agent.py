from langdetect import detect

def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    Returns ISO language code (en, ta, hi, etc.)
    """
    try:
        return detect(text)
    except:
        return "en"