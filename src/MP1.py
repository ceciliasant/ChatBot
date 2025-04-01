import re
import os
from datetime import datetime  # Para timestamp nos ficheiros

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
# Função para limpar artigos das entidades
# --------------------------
def clean_entity(text):
    return re.sub(r"^(the|a|an)\\s+", "", text.strip(), flags=re.IGNORECASE)

# --------------------------
# 6. Loop Principal de Conversação
# --------------------------
def main_chat_loop():
    user_id = "user_123"
    session = generateSession()

    print("Bot: Hello! I'm your knowledge assistant. Type 'exit' to end.")
    conversation_log = []

    while True:
        user_input = input("You: ").strip()
        conversation_log.append(f"You: {user_input}")

        if user_input.lower() == 'exit':
            break

        # Verificação gramatical
        matches = grammar_tool.check(user_input)
        filtered_matches = [match for match in matches if match.ruleId not in ignored_spellcheck_rules]

        for match in filtered_matches:
            suggestion = grammar_tool.correct(user_input)
            print(f"Bot: Did you mean: '{suggestion}'? [Y/N]")
            conversation_log.append(f"Bot: Did you mean: '{suggestion}'? [Y/N]")
            confirm = input("You: ").lower()
            conversation_log.append(f"You: {confirm}")
            if confirm in ["s", "sim", "y", "yes"]:
                user_input = suggestion
                break

        # Detectar intenção
        intent = detect_intent(user_input)

        # Processar intenções
        if intent == "greet":
            response = "Hello! How can I help you today?"
            print(f"Bot: {response}")
            conversation_log.append(f"Bot: {response}")

        elif intent == "store_fact":
            if match := re.search(r"^(.+?) (" + "|".join(map(re.escape, RELATION_KEYS)) + r") (.+?)(\.|$)", user_input, re.IGNORECASE):
                entity, relation_type, state = clean_entity(match.group(1)), match.group(2), match.group(3)
                existing_fact = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type=relation_type).first()

                if existing_fact:
                    if existing_fact.value.lower() == state.lower():
                        response = f"You already told me that {entity} {relation_type} {state}."
                    else:
                        prompt = f"You said before that {entity} {relation_type} {existing_fact.value}. Do you want to update it? [Y/N]"
                        print(f"Bot: {prompt}")
                        conversation_log.append(f"Bot: {prompt}")
                        answer = input("You: ").strip().lower()
                        conversation_log.append(f"You: {answer}")
                        if answer in ["y", "yes", "s", "sim"]:
                            existing_fact.value = state.lower()
                            session.commit()
                            response = f"Updated! {entity.capitalize()} {relation_type} {state}."
                        else:
                            response = "Got it. I won't change anything."
                else:
                    session.add(UserFact(user_id=user_id, key=entity.lower(), value=state.lower(), fact_type=relation_type))
                    session.commit()
                    response = f"Noted! {entity.capitalize()} {relation_type} {state}."
            else:
                response = "I don't know how to process this information!"

            print(f"Bot: {response}")
            conversation_log.append(f"Bot: {response}")



        elif intent == "retrieve_info":

            # WEATHER
            if match := re.search(r"weather|rain|sun|temperature", user_input, re.IGNORECASE):
                city_match = re.search(r"in (\w+)", user_input, re.IGNORECASE)
                city = city_match.group(1) if city_match else "Aveiro"
                weather_info = get_weather(city)
                print(f"Bot: {weather_info}")
                conversation_log.append(f"Bot: {weather_info}")

            # UPDATE FACT
            elif match := re.search(r"what is the (\w+) of (.+?)(\?|$)", user_input, re.IGNORECASE):
                attribute, entity = match.group(1), clean_entity(match.group(2))

                fact = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type="is").order_by(UserFact.id.desc()).first()

                if fact:
                    response = f"The {attribute} of the {entity} is {fact.value}."
                else:
                    response = f"I don't know the {attribute} of the {entity}."

                print(f"Bot: {response}")
                conversation_log.append(f"Bot: {response}")



            # IS/ARE
            elif match := re.search(r"^(" + "|".join(map(re.escape, RELATION_VALUES)) + r") (is|are) (.+?)(\?|$)", user_input, re.IGNORECASE):
                relation_type, entity = match.group(1), clean_entity(match.group(3))
                r_keys = get_relation_key(relation_type.lower())

                alias_list = [entity]
                alias_facts = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type="is a")
                for row in alias_facts:
                    alias_list.append(row.value)

                gotAFact = False
                for alias in alias_list:
                    for relation_key in r_keys:
                        fact = session.query(UserFact).filter_by(user_id=user_id, key=alias.lower(), fact_type=relation_key).order_by(UserFact.id.desc()).first()
                        if fact:
                            gotAFact = True
                            response = f"The {entity.capitalize()} {fact.fact_type} {fact.value}."
                            print(f"Bot: {response}")
                            conversation_log.append(f"Bot: {response}")
                            break
                    if gotAFact:
                        break

                if not gotAFact:
                    response = f"I don't know anything about {user_input.lower()[:-1]}."
                    print(f"Bot: {response}")
                    conversation_log.append(f"Bot: {response}")



            # WHAT/WHERE DOES/did
            elif match := re.search(r"^(What|Where|Who) (does|did) (.+?) (" + "|".join(map(re.escape, RELATION_VALUES)) + r")(\?|$)", user_input, re.IGNORECASE):
                entity, relation_type = clean_entity(match.group(3)), match.group(4)
                r_keys = get_relation_key(relation_type.lower())

                alias_list = [entity]
                alias_facts = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type="is a")
                for row in alias_facts:
                    alias_list.append(row.value)

                gotAFact = False
                for alias in alias_list:
                    for relation_key in r_keys:
                        fact = session.query(UserFact).filter_by(user_id=user_id, key=alias.lower(), fact_type=relation_key).order_by(UserFact.id.desc()).first()
                        if fact:
                            gotAFact = True
                            response = f"{entity.capitalize()} {fact.fact_type} {fact.value}."
                            print(f"Bot: {response}")
                            conversation_log.append(f"Bot: {response}")
                            break
                    if gotAFact:
                        break

                if not gotAFact:
                    response = f"I don't know anything about {user_input.lower()[:-1]}."
                    print(f"Bot: {response}")
                    conversation_log.append(f"Bot: {response}")


            # WHAT/WHERE/WHO does WHAT
            elif match := re.search(r"^(What|Where|Who) (" + "|".join(map(re.escape, RELATION_KEYS)) + r") (.+?)(\?|$)", user_input, re.IGNORECASE):
                entity, relation_type = clean_entity(match.group(3)), match.group(2)

                alias_list = [entity]
                alias_facts = session.query(UserFact).filter_by(user_id=user_id, key=entity.lower(), fact_type="is a")
                for row in alias_facts:
                    alias_list.append(row.value)

                gotAFact = False
                for alias in alias_list:
                    fact = session.query(UserFact).filter_by(user_id=user_id, value=alias.lower(), fact_type=relation_type).order_by(UserFact.id.desc()).first()
                    if fact:
                        gotAFact = True
                        response = f"{fact.key.capitalize()} {fact.fact_type} {entity}."
                        print(f"Bot: {response}")
                        conversation_log.append(f"Bot: {response}")
                        break

                if not gotAFact:
                    response = f"I don't know anything about {user_input.lower()[:-1]}."
                    print(f"Bot: {response}")
                    conversation_log.append(f"Bot: {response}")

            else:
                response = "Could you specify what you're asking about?"
                print(f"Bot: {response}")
                conversation_log.append(f"Bot: {response}")

        else:  # Fallback generativo
            response = generate_response(user_input)
            print(f"Bot: {response}")
            conversation_log.append(f"Bot: {response}")

    # --------------------------
    # Gravação da conversa
    # --------------------------
    save = input("Bot: Do you want to save this conversation? [Y/N]\nYou: ").strip().lower()
    conversation_log.append(f"You: {save}")
    if save in ["y", "yes", "s", "sim"]:
        file_name = input("Bot: What should be the name of the file?\nYou: ").strip()
        conversation_log.append(f"You: {file_name}")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs("chats", exist_ok=True)
        path = os.path.join("chats", f"{file_name}_{timestamp}.txt")
        with open(path, "w", encoding="utf-8") as f:
            for line in conversation_log:
                f.write(line + "\n")
        print(f"Bot: Conversation saved to {path}. Goodbye!")
    else:
        print("Bot: Alright, goodbye!")

if __name__ == "__main__":
    main_chat_loop()
