import re
from know_manipulation.fact_types import RELATION_KEYS

intent_patterns = {
    "greet": r"^hello|hi|hey",
    "retrieve_info": r"^.*\?$",
    "ask_weather": r"weather|rain|sun|temperature",
    "store_fact": r"^(.+?) (" + "|".join(map(re.escape, RELATION_KEYS)) + r") (.+?)(\.|$)",
    "vague_prompt": r"tell me something|something interesting|a fact",
    "social": r"\b(thanks|thank you)\b",
}