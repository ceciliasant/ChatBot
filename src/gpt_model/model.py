from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define o token de padding para evitar erros
tokenizer.pad_token = tokenizer.eos_token  

def generate_response(user_input, max_length=200):
    persona = (
        "System: You are an AI assistant specialized in knowledge-based chatbots. "
        "Your role is to help refine user requests so they can be correctly interpreted by a chatbot. "
        "If the chatbot does not understand the user's intent, your job is to ask the user to clarify or reformulate their message. "
        "Always be concise and stay on topic. Do not provide responses outside of this scope. "
        "Example: If the user asks 'Tell me something interesting,' you should reply: "
        "'Could you clarify what topic interests you?' "
        "User: \n"
    )

    full_prompt = persona + user_input + tokenizer.eos_token

    # Gera os tokens e a máscara de atenção corretamente
    inputs = tokenizer(
        full_prompt,
        return_tensors="pt",
        padding=True,
        truncation=False
    )

    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    response_ids = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        pad_token_id=tokenizer.eos_token_id,
        top_k=5,  # Reduzindo para permitir alguma variação, mas mantendo foco
        top_p=0.7,  # Restringe a escolha de tokens mais prováveis
        temperature=0.5,  # Reduzindo para tornar respostas mais determinísticas
        do_sample=True,
        repetition_penalty=1.5  # Penaliza repetições para evitar frases redundantes
        )

    return tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

