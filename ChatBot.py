# Libraries
import json
from textblob import TextBlob
import os
import re
import random

# Load or initialize knowledge base
KNOWLEDGE_FILE = 'knowledge.json'
BOT_NAME = "Ciri"

if os.path.exists(KNOWLEDGE_FILE):
    with open(KNOWLEDGE_FILE, 'r') as f:
        knowledge = json.load(f)
else:
    knowledge = {}

def save_knowledge():
    with open(KNOWLEDGE_FILE, 'w') as f:
        json.dump(knowledge, f, indent=4)

def correct_grammar(sentence):
    blob = TextBlob(sentence)
    return str(blob.correct())

def learn_fact(user_input):
    if user_input.strip().endswith("?") or user_input.lower().startswith("what"):
        return None

    # Learn facts from "X is Y"
    elif " is " in user_input:
        parts = user_input.split(" is ")
        if len(parts) == 2:
            key = parts[0].strip().lower()
            value = parts[1].strip()
            knowledge[key] = value
            save_knowledge()
            return f"Got it! I'll remember that {key} is {value}."
    return None

def recall_fact(user_input):
    if "your name" in user_input.lower():
        return f"My name is {BOT_NAME}."
    
    # Match patterns like: "What is X?"
    match = re.search(r'what is (.*)\??', user_input.lower())
    if match:
        key = match.group(1).strip()
        if key in knowledge:
            return f"You told me that {key} is {knowledge[key]}."
    # Fallback to normal partial matching
    for key in knowledge:
        if key in user_input.lower():
            return f"You told me that {key} is {knowledge[key]}."
    return None

def fallback():
    responses = [
        "Hmm, that's interesting! Can you tell me more?",
        "I'm not sure I understood that. Could you rephrase?",
        "That's new to me. Care to explain?"
    ]
    return random.choice(responses)

def chatbot_response(user_input):
    # Learn new fact
    learned = learn_fact(user_input)
    if learned:
        return learned

    # Check memory for stored facts
    recall = recall_fact(user_input)
    if recall:
        return recall

    # Simple greetings
    greetings = ["hello", "hi", "olá", "hey"]
    if any(greet in user_input.lower() for greet in greetings):
        return "Hello! How can I help you?"

    # Try grammar correction
    skip_correction_keywords = ["what", "who","where", "are you", "my name", "your name"]
    if not any(kw in user_input.lower() for kw in skip_correction_keywords):
        corrected = correct_grammar(user_input)
        if corrected != user_input:
            return f"I think you meant: '{corrected}'"

    # Fallback
    return fallback()

# ===== MAIN LOOP =====
print("Chatbot is running. Type 'exit' to stop.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break
    response = chatbot_response(user_input)
    print(f"Bot: {response}")
