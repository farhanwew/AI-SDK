import os 
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

message = input("Enter your message: ")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[{"role": "user", "content": f"{message}"}]
)

asistant_message = response.choices[0].message.content
print("Assistant:", asistant_message)