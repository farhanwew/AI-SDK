# sliding_window memory example
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


treshold = 5

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def sliding_window():
    messages = []

    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break

        if len(messages) > treshold:
            messages = messages[1:]

        messages.append({ "role": "user", "content": user_input })

        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages
        )

        assistant_response = response.choices[0].message.content
        messages.append({ "role": "assistant", "content": assistant_response })
        print(assistant_response)

    print(messages)

sliding_window()