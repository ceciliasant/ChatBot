import re

# --------------------------
# 1. Import language processing
# --------------------------
from lang_processing.processing import grammar_tool
from lang_processing.processing import nlp

# --------------------------
# 2. Import knowledge manipulation
# --------------------------
from know_manipulation.know_storage import session
from know_manipulation.user_fact import UserFact

# --------------------------
# 2. Import backup language model (DialoGPT)
# --------------------------
from gpt_model.model import generate_response

# --------------------------
# 4. Detecção de Intenções (Corrigida)
# --------------------------
from lang_processing.processing import detect_intent

# --------------------------
# 5. Loop Principal de Conversação
# --------------------------
def main_chat_loop():
    user_id = "user_123"
    
    print("Bot: Hello! I'm your knowledge assistant. Type 'exit' to end.")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() == 'exit':
                break

            # Verificação gramatical
            matches = grammar_tool.check(user_input)
            if matches:
                print(f"Bot: Did you mean: '{grammar_tool.correct(user_input)}'?")
                continue

            # Detectar intenção
            intent = detect_intent(user_input)

            # Processar intenções
            if intent == "greet":
                print("Bot: Hello! How can I help you today?")
            
            elif intent == "store_fact":
                if match := re.search(r"(?:the|a|my) (\w+) (is|are) (.+?)(\.|$)", user_input, re.IGNORECASE):
                    entity, state = match.group(1), f"{match.group(2)} {match.group(3)}"
                    session.add(UserFact(user_id=user_id, key=entity, value=state))
                    session.commit()
                    print(f"Bot: Okay, I'll remember that {entity} {state}.")
            
            elif intent == "store_general":
                if match := re.search(r"^(.+?) (is|are) (.+?)(\.|$)", user_input, re.IGNORECASE):
                    entity, state = match.group(1), f"{match.group(2)} {match.group(3)}"
                    session.add(UserFact(user_id=user_id, key=entity, value=state))
                    session.commit()
                    print(f"Bot: Noted! {entity.capitalize()} {state}.")
            
            elif intent == "retrieve_info":
                doc = nlp(user_input)
                entity = next((token.text.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]), None)
                
                if entity:
                    fact = session.query(UserFact).filter_by(user_id=user_id, key=entity).first()
                    if fact:
                        print(f"Bot: {entity.capitalize()} {fact.value}.")
                    else:
                        print(f"Bot: I don't know anything about {entity}.")
                else:
                    print("Bot: Could you specify what you're asking about?")
            
            elif intent == "ask_weather":
                print("Bot: Currently, it's sunny with 25°C. (Weather API placeholder)")

            else:  # Fallback generativo
                response = generate_response(user_input)
                print(f"Bot: {response}")

        except Exception as e:
            print(f"Bot: Sorry, I encountered an error. ({str(e)})")

if __name__ == "__main__":
    main_chat_loop()