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
# 3. Import backup language model (DialoGPT)
# --------------------------
from gpt_model.model import generate_response

# --------------------------
# 4. Import external APIs
# --------------------------
from external_apis.weather import get_weather

# --------------------------
# 5. Detecção de Intenções (Corrigida)
# --------------------------
from lang_processing.processing import detect_intent

# --------------------------
# 6. Loop Principal de Conversação
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
            if match := re.search(r"^(.+?) (" + "|".join(map(re.escape, RELATION_KEYS)) + r") (.+?)(\.|$)", user_input, re.IGNORECASE):
                entity, relation_type, state = match.group(1).split(" ")[-1], match.group(2), match.group(3).split(" ")[-1]
                existing_fact = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type=relation_type).first()
                
                if existing_fact:
                    if existing_fact.value.lower() == state.lower():
                        print(f"Bot: You already told me that {entity} {relation_type} {state}.")
                    else:
                        print(f"Bot: You said before that {entity} {relation_type} {existing_fact.value}. Do you want to update it? [Y/N]")
                        answer = input("You: ").strip().lower()
                        if answer in ["y", "yes", "s", "sim"]:
                            existing_fact.value = state.lower()
                            session.commit()
                            print(f"Bot: Updated! {entity.capitalize()} {relation_type} {state}.")
                        else:
                            print("Bot: Got it. I won't change anything.")
                else:
                    session.add(UserFact(user_id=user_id, key=entity.lower(), value=state.lower(), fact_type=relation_type))
                    session.commit()
                    print(f"Bot: Noted! {entity.capitalize()} {relation_type} {state}.")
            else:
                print("Bot: I don't know how to process this information!")

        
        elif intent == "retrieve_info":
            
            
            #  WEATHER
            if match := re.search(r"weather|rain|sun|temperature", user_input, re.IGNORECASE):
                city_match = re.search(r"in (\w+)", user_input, re.IGNORECASE)
                city = city_match.group(1) if city_match else "Aveiro"
                weather_info = get_weather(city)
                print(f"Bot: {weather_info}")

            #  IS/ARE
            elif match := re.search(r"^(" + "|".join(map(re.escape, RELATION_VALUES)) + r") (is|are) (.+?)(\?|$)", user_input, re.IGNORECASE):
                relation_type, entity = match.group(1), match.group(3).split(" ")[-1]

                #  Get type of question
                r_keys = get_relation_key(relation_type.lower())

                alias_list = [entity]

                #  Search for alias or other "is_a" relations for the subject
                alias_facts = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type="is a")                

                for row in alias_facts:
                    alias_list.append(row.value)

                gotAFact = False

                for alias in alias_list:
                    for relation_key in r_keys:
                        fact = session.query(UserFact).filter_by(user_id=user_id, key=alias.lower(), fact_type=relation_key).order_by(UserFact.id.desc()).first()
                    
                        if fact:
                            gotAFact = True
                            print(f"Bot: The {entity.capitalize()} {fact.fact_type} the {fact.value}.")
                            break
                    
                    if fact:
                        break

                if not gotAFact:
                    print(f"Bot: I don't know anything about {user_input.lower()[:-1]}.")

            #  WHAT/WHERE DOES/did
            elif match := re.search(r"^(What|Where|Who) (does|did) (.+?) (" + "|".join(map(re.escape, RELATION_VALUES)) + r")(\?|$)", user_input, re.IGNORECASE):
                entity, relation_type = match.group(3).split(" ")[-1], match.group(4)

                #  Get type of question
                r_keys = get_relation_key(relation_type.lower())

                alias_list = [entity]

                #  Search for alias or other "is_a" relations for the subject
                alias_facts = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type="is a")                

                for row in alias_facts:
                    alias_list.append(row.value)

                gotAFact = False

                for alias in alias_list:
                    for relation_key in r_keys:
                        fact = session.query(UserFact).filter_by(user_id=user_id, key=alias.lower(), fact_type=relation_key).order_by(UserFact.id.desc()).first()
                    
                        if fact:
                            gotAFact = True
                            print(f"Bot: {entity.capitalize()} {fact.fact_type} {fact.value}.")
                            break
                    
                    if gotAFact:
                        break

                if not gotAFact:
                    print(f"Bot: I don't know anything about {user_input.lower()[:-1]}.")
            
            #  WHAT/WHERE/WHO does WHAT
            elif match := re.search(r"^(What|Where|Who) (" + "|".join(map(re.escape, RELATION_KEYS)) + r") (.+?)(\?|$)", user_input, re.IGNORECASE):

                entity, relation_type = match.group(3).split(" ")[-1], match.group(2)

                alias_list = [entity]

                #  Search for alias or other "is_a" relations for the subject
                alias_facts = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type="is a")                

                for row in alias_facts:
                    alias_list.append(row.value)

                gotAFact = False

                for alias in alias_list:
                    fact = session.query(UserFact).filter_by(user_id=user_id, value=alias.lower(), fact_type=relation_type).order_by(UserFact.id.desc()).first()
                
                    if fact:
                        gotAFact = True
                        print(f"Bot: {fact.key.capitalize()} {fact.fact_type} {entity}.")
                        break
                

                if not gotAFact:
                    print(f"Bot: I don't know anything about {user_input.lower()[:-1]}.")
            
            else:
                print("Bot: Could you specify what you're asking about?")

        else:  # Fallback generativo
            response = generate_response(user_input)
            print(f"Bot: {response}")

        """ except Exception as e:
            print(f"Bot: Sorry, I encountered an error. ({str(e)})") """

if __name__ == "__main__":
    main_chat_loop()