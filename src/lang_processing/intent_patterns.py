intent_patterns = {
    "greet": r"^hello|hi|hey",
    "retrieve_info": r"^(what|where|who).*\?$",
    "ask_weather": r"weather|rain|sun|temperature",
    "store_fact": r"(the|a|my) (\w+) (is|are) (on|in|at|a) (.+?)(\.|$)",
    "store_general": r"^([^?]+) (is|are) (.+?)(\.|$)"
}