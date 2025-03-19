import re
import spacy
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from transformers import AutoTokenizer, AutoModelForCausalLM
from language_tool_python import LanguageTool

# --------------------------
# 1. Configuração Inicial
# --------------------------

# NLP com spaCy
nlp = spacy.load("en_core_web_sm")

# Verificação gramatical
tool = LanguageTool('en-US')

# --------------------------
# 2. Base de Conhecimento (SQLite)
# --------------------------
Base = declarative_base()

class UserFact(Base):
    __tablename__ = 'user_facts'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    key = Column(String)  # Entidade (ex: "cat")
    value = Column(String)  # Fato (ex: "is on the floor")

engine = create_engine('sqlite:///knowledge.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --------------------------
# 3. Modelo de Linguagem (DialoGPT)
# --------------------------
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(user_input, max_length=100):
    input_ids = tokenizer.encode(
        user_input + tokenizer.eos_token,
        return_tensors="pt"
    )
    response_ids = model.generate(
        input_ids,
        max_length=max_length,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_p=0.95,
        no_repeat_ngram_size=3
    )
    return tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

# --------------------------
# 4. Detecção de Intenções (Corrigida)
# --------------------------
intent_patterns = {
    "greet": r"^hello|hi|hey",
    "retrieve_info": r"^(what|where|who).*\?$",
    "ask_weather": r"weather|rain|sun|temperature",
    "store_fact": r"(the|a|my) (\w+) (is|are) (on|in|at|a) (.+?)(\.|$)",
    "store_general": r"^([^?]+) (is|are) (.+?)(\.|$)"
}

def detect_intent(text):
    text = text.lower().strip()
    for intent, pattern in intent_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return intent
    return "unknown"

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
            matches = tool.check(user_input)
            if matches:
                print(f"Bot: Did you mean: '{tool.correct(user_input)}'?")
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