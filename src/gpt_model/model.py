from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Configuração correta para T5 (não force pad_token = eos_token!)
tokenizer.pad_token = tokenizer.eos_token  # Opcional, apenas se necessário

def generate_response(user_input):  
    prompt = f"Explain in 1-2 sentences, factually and clearly: {user_input}"  
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)  
    outputs = model.generate(**inputs, max_length=200)  
    return tokenizer.decode(outputs[0], skip_special_tokens=True)  

# def generate_response(user_input, max_length=400):
#     # Adicione um prefixo de tarefa claro ao prompt
#     persona = (
#         "System: You are an AI assistant specialized in knowledge-based chatbots. "
#         "Your role is to help refine user requests so they can be correctly interpreted by a chatbot. "
#         "If the chatbot does not understand the user's intent, your job is to say that you don't know the answer or don't understand the question and nothing more. "
#         "Always be concise and stay on topic. Do not provide responses outside of this scope. "
#         "And don't say 'There is no X at your location' or 'There is no X in your area' or something similar \n "
#         "User: "
#     )

#     full_prompt = persona + user_input  # Remova o eos_token manual

#     inputs = tokenizer(
#         full_prompt,
#         return_tensors="pt",
#         padding="max_length",  # Forçar padding consistente
#         truncation=True,
#         max_length=512  # T5 tem limite de 512 tokens
#     )

#     # Geração ajustada para T5
#     response_ids = model.generate(
#         input_ids=inputs.input_ids,
#         attention_mask=inputs.attention_mask,
#         max_length=max_length,
#         temperature=0.7,  # Mais flexibilidade
#         top_k=50,
#         top_p=0.95,
#         repetition_penalty=1.2,
#         do_sample=True,
#         num_beams=3  # Busca em feixe para melhor coerência
#     )
    
#     return tokenizer.decode(response_ids[0], skip_special_tokens=True)