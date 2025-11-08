from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

class Event(BaseModel):
    name: str
    job_title: str
    description: str
    date: str
    location: str
# completion parse

response = client.chat.completions.parse(
    model="gpt-5-nano",
    messages=[
        { "role": "user", "content": "I'd like to meet with Brian 12 Sep 2025, 12AM at City Hall. He is a product manager."}
    ],
    response_format=Event,
)

assistant_response = response.choices[0].message.parsed
print(assistant_response.model_dump())