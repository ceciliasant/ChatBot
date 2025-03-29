import re

# --------------------------
# 1. Import language processing
# --------------------------
from lang_processing.processing import grammar_tool
from lang_processing.processing import nlp
from lang_processing.processing import ignored_spellcheck_rules

# --------------------------
# 2. Import knowledge manipulation
# --------------------------
from know_manipulation.know_storage import generateSession
from know_manipulation.user_fact import UserFact
from know_manipulation.fact_types import RELATION_KEYS, RELATION_VALUES, get_relation_key

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

    session = generateSession()
    
    print("Bot: Hello! I'm your knowledge assistant. Type 'exit' to end.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            break

        # Verificação gramatical
        matches = grammar_tool.check(user_input)
        
        filtered_matches = [match for match in matches if match.ruleId not in ignored_spellcheck_rules]

        # Display filtered matches
        for match in filtered_matches:
            print(f"Bot: Did you mean: '{grammar_tool.correct(user_input)}'? [Y/N]")
            if input("You: ").lower() in ["s, sim, y, yes"]:
                user_input = match
                break
            

        # Detectar intenção
        intent = detect_intent(user_input)

        # Processar intenções
        if intent == "greet":
            print("Bot: Hello! How can I help you today?")
        
        elif intent == "store_fact":
            #if match := re.search(r" (?:the|a|my) (\w+) (is|are) (.+?)(\.|$)", user_input, re.IGNORECASE):
            if match := re.search(r"^(.+?) (" + "|".join(map(re.escape, RELATION_KEYS)) + r") (.+?)(\.|$)", user_input, re.IGNORECASE):
                entity, relation_type, state = match.group(1), match.group(2), match.group(3)
                session.add(UserFact(user_id=user_id, key=entity.lower(), value=state, fact_type=relation_type))
                session.commit()
                print(f"Bot: Noted! {entity.capitalize()} {relation_type} {state}.")
            else:
                print("Bot: I don't know how to process this information!")
        
        elif intent == "retrieve_info":
            
            #  IS/ARE
            if match := re.search(r"^(" + "|".join(map(re.escape, RELATION_VALUES)) + r") (is|are) (.+?)(\?|$)", user_input, re.IGNORECASE):
                relation_type, entity = match.group(1), match.group(3)

                #  Get type of question
                r_keys = get_relation_key(relation_type.lower())

                gotAFact = False

                for relation_key in r_keys:
                    fact = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type=relation_key).order_by(UserFact.id.desc()).first()
                
                    if fact:
                        gotAFact = True
                        print(f"Bot: {entity.capitalize()} {fact.fact_type} {fact.value}.")
                        break

                if (gotAFact == False):
                    print(f"Bot: I don't know anything about {relation_type.lower()} is {entity}.")
            

            #  WHAT/WHERE DOES/did
            elif match := re.search(r"^(What|Where) (does|did) (.+?) (" + "|".join(map(re.escape, RELATION_VALUES)) + r")(\?|$)", user_input, re.IGNORECASE):
                entity, relation_type = match.group(3), match.group(4)

                #  Get type of question
                relation_key = get_relation_key(relation_type.lower())

                fact = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type=relation_key).order_by(UserFact.id.desc()).first()
                
                if fact:
                    print(f"Bot: {entity.capitalize()} {fact.fact_type} {fact.value}.")
                else:
                    print(f"Bot: I don't know anything about {relation_type.lower()} is {entity}.")
            
            else:
                print("Bot: Could you specify what you're asking about?")
        
        elif intent == "ask_weather":
            print("Bot: Currently, it's sunny with 25°C. (Weather API placeholder)")

        else:  # Fallback generativo
            response = generate_response(user_input)
            print(f"Bot: {response}")

        """ except Exception as e:
            print(f"Bot: Sorry, I encountered an error. ({str(e)})") """

if __name__ == "__main__":
    main_chat_loop()