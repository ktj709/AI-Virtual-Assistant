import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def get_intent(text):
    text = text.lower()
    doc = nlp(text)
    if any(w in text for w in ["calculate", "solve", "plus", "minus", "times", "multiply", "divide", "into", "by"]):
        return "math"
    elif "remind" in text or "reminder" in text:
        return "reminder"
    elif "search" in text or "find" in text:
        return "search"
    elif "weather" in text or "temperature" in text:
        return "weather"
    elif "open" in text and ("browser" in text or "google" in text):
        return "open_browser"
    elif "time" in text and "times" not in text:
        return "time"
    else:
        return "chat"
