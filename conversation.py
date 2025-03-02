# import openai
# import os

# GPT_API_KEY = os.getenv("GPT_API_KEY")

# def process_conversation(user_input):
#     if not GPT_API_KEY:
#         return "Error: OpenAI API key is missing."

#     try:
#         openai.api_key = GPT_API_KEY
#         response = openai.ChatCompletion.create(
#             model="gpt-4o",
#             messages=[{"role": "user", "content": user_input}]
#         )
#         return response["choices"][0]["message"]["content"]
#     except openai.error.OpenAIError as e:
#         return f"Error: {str(e)}"


import openai
import os

GPT_API_KEY = os.getenv("GPT_API_KEY")

def process_conversation(user_input):
    if not GPT_API_KEY:
        return "Error: OpenAI API key is missing."
    openai.api_key = GPT_API_KEY

    try:
        response = openai.ChatCompletion.create(

        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    except openai.error.OpenAIError as e:
        return f"Error: {str(e)}"
    return response["choices"][0]["message"]["content"]


def store_conversation(phone_number, conversation_data):
    """Stores conversation history for a phone number."""
    with open(f"conversations/{phone_number}.txt", "w") as file:
        for message in conversation_data:
            file.write(f"{message['role']}: {message['content']}\n")
