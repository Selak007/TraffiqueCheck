from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Clear cache
cached_path.cache.clear()
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Initialize chat history
chat_history_ids = None

# Function to generate chatbot response
def chatbot_response(user_input):
    global chat_history_ids

    # Encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append the new user input tokens to the chat history
    # If there's no previous chat history, this will just be the new input
    bot_input_ids = new_user_input_ids if chat_history_ids is None else torch.cat([chat_history_ids, new_user_input_ids], dim=-1)

    # Generate a response from the model
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, no_repeat_ngram_size=3, temperature=0.7)

    # Decode the generated response and return it
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return bot_response

# Example conversation
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    response = chatbot_response(user_input)
    print(f"Bot: {response}")
