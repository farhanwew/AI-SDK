from openai import OpenAI
import os
from dotenv import load_dotenv
import json

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


def function_tool_process():
    user_input = input("User: ")
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            { "role": "system", "content": "use `multiply_tool` if user ask to multiply numbers" },
            { "role": "user", "content": user_input }
        ],
        tools=[multiply_tool] #type: ignore
    )

    assistant_response = response.choices[0].message
    print(assistant_response)
    if assistant_response.tool_calls:
        tool_results = []

        for tool_call in assistant_response.tool_calls:
            if tool_call.function.name == "multiply":
                args = json.loads(tool_call.function.arguments)
                result = multiply(**args)
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": str(result)
                })

        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_input},
                assistant_response, #type: ignore
                *tool_results
            ]
        )

        print(final_response.choices[0].message.content)
    else:
        print(assistant_response.content)

function_tool_process()