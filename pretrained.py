#https://github.com/microsoft/DialoGPT


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

def chat(sentences):
  user_input_ids = tokenizer.encode(sentences + tokenizer.eos_token, return_tensors='pt')
  response_ids = model.generate(user_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
  bot_response = response_ids[0][len(user_input_ids[0]):]

  return tokenizer.decode(bot_response, skip_special_tokens=True)