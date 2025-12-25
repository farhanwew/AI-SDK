from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

base_url="https://openrouter.ai/api/v1"

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=base_url
)

response = client.chat.completions.create(
    model="meta-llama/llama-4-maverick:freet",
    messages=[{ "role": "user", "content": "Who are you ?"}]
)

assistant_response = response.choices[0].message.content
print(assistant_response)