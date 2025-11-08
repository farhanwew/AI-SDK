from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

CONTENT = """
    Farhan is a software developer from Indonesia who specializes in AI and machine learning. He has worked on various projects involving natural language processing and computer vision. 
    In his free time
    """

response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
            { "role": "system", "content": f"Always answer based on context. Context: {CONTENT}"},
            { "role": "user", "content": "Do you know Farhan?"}
        ],
)

assistant_response = response.choices[0].message.content
print(assistant_response)