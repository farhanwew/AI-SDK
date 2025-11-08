from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def summarized_based_context():
    conversation_summary = ""
    messages = []

    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break

        messages.append({"role": "user", "content": user_input})
        
        print("message now:", messages)
        print("summary now:", conversation_summary)

        context = []
        if conversation_summary:
            context.append({
                "role": "system",
                "content": f"Previous conversation summary: {conversation_summary}"})

        context.extend(messages)
        
        print("context now:", context)
         
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=context
        )

        assistant_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_response})
        print(assistant_response)

        # Summarize
        if len(messages) > 6:
            print("Summarizing conversation...")
            summary_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Summarize this conversation briefly:"}] + messages[:-2] #type: ignore
            )

            conversation_summary = summary_response.choices[0].message.content
            #last two messages are kept for context
            messages = messages[-2:]

    print(messages)

summarized_based_context()