# in this example, the funtion is failed to be called and the llm didnt give any content outputm, becasuse
# we didnt process the tool call and give the result back to llm for final answer generation
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def multiply(a, b):
    return a * b

multiply_tool = {
    "type": "function",
    "function": {
        "name": "multiply",
        "description": "Multiplies two numbers together and returns the product.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "The first number to multiply"
                },
                "b": {
                    "type": "number",
                    "description": "The second number to multiply"
                }
            },
            "required": ["a", "b"]
        }
    }
}

def function_tool():
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{ "role": "user", "content": "What is 99541 * 6956 "}],
        tools=[multiply_tool] #type: ignore
    )

    assistant_response = response.choices[0].message
    print(assistant_response)
    print("Tool Calls:", assistant_response.tool_calls)

function_tool()