from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(user_input, max_length=100):
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        
    input_ids = tokenizer.encode(
        user_input + tokenizer.eos_token,
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
