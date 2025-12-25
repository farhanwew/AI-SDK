import json
from agents import Agent, Runner, function_tool, RunContextWrapper
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class UserInfo:
    id: str

@function_tool
def get_user_info(wrapper: RunContextWrapper[UserInfo]) -> str:
    return json.dumps({"id": wrapper.context.id, "name": "John Doe", "email": "john.doe@example.com", "phone": "123-456-7890"})

async def main():
    messages = []

    user_info = UserInfo(id="sk-123")

    assistant_agent = Agent[UserInfo](
        name="Assistant",
        instructions="You are helpful assistant",
        model="gpt-5-mini",
        tools=[get_user_info]
    )

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})
        runner = await Runner.run(starting_agent=assistant_agent, input=messages, context=user_info)
        messages = runner.to_input_list()

        print(runner.last_agent.name)
        print(runner.final_output)
        print("===" * 20)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())