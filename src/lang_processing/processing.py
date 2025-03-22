import re
import spacy
from language_tool_python import LanguageTool

from lang_processing.intent_patterns import intent_patterns


# NLP com spaCy
nlp = spacy.load("en_core_web_sm")

# Verificação gramatical
grammar_tool = LanguageTool('en-US')

def detect_intent(text):
    text = text.lower().strip()
    for intent, pattern in intent_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return intent
    return "unknown"