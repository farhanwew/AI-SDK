from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

async def main():
    messages = []

    assistant_agent = Agent(
        name="Assistant",
        instructions="You are helpful assistant",
        model="gpt-5-mini",
    )

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})
        runner = await Runner.run(starting_agent=assistant_agent, input=messages)
        messages = runner.to_input_list()
        print(runner.last_agent.name)
        print(runner.final_output)
        print("===" * 20)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())