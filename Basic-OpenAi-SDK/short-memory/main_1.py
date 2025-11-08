from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

messages = []

while True:
    
    print(messages)
    user_input = input("User: ")
    if user_input == "exit":
        break

    messages.append({ "role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    print(assistant_response)
    messages.append({ "role": "assistant", "content": assistant_response})

print(messages)