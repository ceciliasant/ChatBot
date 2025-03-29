from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(user_input, max_length=100):
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})

    persona = ("System: You are a knowledge assistant. The user enters requests to impart knowledge to a chatbot, which is done with logic. "
    "If a message from the user reaches you because the chatbot doesn't know the intent of the user's message, respond by asking the user to reformulate the message, do not deviate from these instructions.  \n"
    )

    full_prompt = persona + user_input + tokenizer.eos_token

    input_ids = tokenizer.encode(
        full_prompt,
        return_tensors="pt",
        padding=True
    )
    
    #attention_mask = input_ids["attention_mask"]

    response_ids = model.generate(
        input_ids,
        max_length=max_length,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        do_sample=True,
        top_p=0.95,
        no_repeat_ngram_size=3,
        #attention_mask=attention_mask
    )
    return tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
