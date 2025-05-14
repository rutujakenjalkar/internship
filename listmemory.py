import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType
from autogen_ext.models.openai import OpenAIChatCompletionClient


api_key=""

async def get_weather(city: str, units: str = "imperial") -> str:
    if units == "imperial":
        return f"The weather in {city} is 73 °F and Sunny."
    elif units == "metric":
        return f"The weather in {city} is 23 °C and Sunny."
    else:
        return f"Sorry, I don't know the weather in {city}."


# Initialize user memory
user_memory = ListMemory()

# Add user preferences to memory
async def main():
    await user_memory.add(MemoryContent(content="The weather should be in metric units", mime_type=MemoryMimeType.TEXT))

    await user_memory.add(MemoryContent(content="Meal recipe must be vegan", mime_type=MemoryMimeType.TEXT))



    assistant_agent = AssistantAgent(
        name="assistant_agent",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key=api_key
        ),
        tools=[get_weather],
        memory=[user_memory],
    )


    # Run the agent with a task.
    stream = assistant_agent.run_stream(task="Give me biryani recipe.")
    await Console(stream)


if __name__=="__main__":
    asyncio.run(main())