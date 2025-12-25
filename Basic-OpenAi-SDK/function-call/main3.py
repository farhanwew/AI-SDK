from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

events_db = [
    {
        "id": 1,
        "event_name": "Konferensi Teknologi Digital Indonesia 2025",
        "datetime": "2025-10-15 09:00:00",
        "location": "Jakarta Convention Center, Jakarta"
    },
    {
        "id": 2,
        "event_name": "Festival Startup Nusantara",
        "datetime": "2025-11-22 14:30:00",
        "location": "Balai Kartini, Jakarta"
    },
    {
        "id": 3,
        "event_name": "Kompetisi Inovasi Mahasiswa Indonesia",
        "datetime": "2025-12-08 18:00:00",
        "location": "Universitas Indonesia, Depok"
    },
    {
        "id": 4,
        "event_name": "Workshop Data Science dan AI",
        "datetime": "2026-01-20 10:00:00",
        "location": "Gedung Cyber 2 Tower, Jakarta"
    }
]


def get_events():
    return events_db

get_events_tool = {
    "type": "function",
    "function": {
        "name": "get_events",
        "description": "Retrieves all events from the events database.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}

def add_event(name, datetime, location):
    new_id = len(events_db) + 1
    new_event = {
        "id": new_id,
        "event_name": name,
        "datetime": datetime,
        "location": location
    }
    events_db.append(new_event)
    return new_event


add_event_tool = {
    "type": "function",
    "function": {
        "name": "add_event",
        "description": "Adds a new event to the events database. Auto-generates unique ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the event"
                },
                "datetime": {
                    "type": "string",
                    "description": "The date and time of the event (YYYY-MM-DD HH:MM:SS format)"
                },
                "location": {
                    "type": "string",
                    "description": "The location where the event will take place"
                }
            },
            "required": ["name", "datetime", "location"]
        }
    }
}

import json

SYSTEM_PROMPT = """
    - use `get_events_tool` to retrieve events
    - use `add_event_tool` to add new events to the database.
    """

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]


def function_tool_process():
    while True:
        print("event:\n", events_db)
        user_input = input("User: ")
        if user_input == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages, #type: ignore
            tools=[get_events_tool, add_event_tool], #type: ignore
        )

        assistant_response = response.choices[0].message
        if assistant_response.tool_calls:
            tool_results = []
            for tool_call in assistant_response.tool_calls:
                if tool_call.function.name == "get_events":
                    result = get_events()
                    tool_results.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_call.function.name,
                            "content": json.dumps(result),
                        }
                    )
                elif tool_call.function.name == "add_event":
                    args = json.loads(tool_call.function.arguments)
                    result = add_event(**args)
                    tool_results.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": tool_call.function.name,
                            "content": json.dumps(result),
                        }
                    )

            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": user_input},
                    assistant_response, #type: ignore
                    *tool_results,
                ],
            )

            result = final_response.choices[0].message.content
            messages.append({"role":"assistant", "content": result})
            print(result)
        else:
            result = assistant_response.content
            messages.append({"role":"assistant", "content": result})
            print(result)


function_tool_process()