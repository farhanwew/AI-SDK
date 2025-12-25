from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    """Get the weather of a city"""

    return f"weather of {city} is sunny with 25°C and there is a light breeze."

async def main():
    messages = []

    assistant_agent = Agent(
        name="Assistant",
        instructions="You are helpful assistant",
        model="gpt-5-mini",
        tools=[get_weather],
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