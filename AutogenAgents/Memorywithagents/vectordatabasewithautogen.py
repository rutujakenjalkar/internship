import asyncio
import os
from pathlib import Path
import chromadb

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.memory.chromadb import ChromaDBVectorMemory, PersistentChromaDBVectorMemoryConfig
from autogen_ext.models.openai import OpenAIChatCompletionClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


api_key=""




async def get_weather(city: str, units: str = "imperial") -> str:
    if units == "imperial":
        return f"The weather in {city} is 73 °F and Sunny."
    elif units == "metric":
        return f"The weather in {city} is 23 °C and Sunny."
    else:
        return f"Sorry, I don't know the weather in {city}."




async def main():
    print("creating a vector database")
    
    chroma_user_memory = ChromaDBVectorMemory(
        config=PersistentChromaDBVectorMemoryConfig(
            collection_name="rutuja",
            persistence_path=os.path.join(str(Path.home()), ".chromadb_autogen"),
            k=2,  # Return top  k results
            score_threshold=0.4,  # Minimum similarity score
        ),
        
    )

    
    # a HttpChromaDBVectorMemoryConfig is also supported for connecting to a remote ChromaDB server

    # Add user preferences to memory
   
    print("adding to memory")
    await chroma_user_memory.add(
            MemoryContent(
                content="The weather should be in metric units",
                mime_type=MemoryMimeType.TEXT,
                metadata={"category": "preferences", "type": "units"},
            )
        )
    

    await chroma_user_memory.add(
        MemoryContent(
            content="Meal recipe must be vegan",
            mime_type=MemoryMimeType.TEXT,
            metadata={"category": "preferences", "type": "dietary"},
        )
    )

    print("creating the model")
    model_client = OpenAIChatCompletionClient(
        model="gemini-1.5-pro",
        api_key=api_key,
       
    )
    model_client.model_info["multiple_system_messages"] = True

    # Create assistant agent with ChromaDB memory
    print("creating the assistant")
    assistant_agent = AssistantAgent(
        name="assistant_agent",
        model_client=model_client,
       tools=[get_weather],
       memory=[chroma_user_memory],
       
    )

    print("print the stream..")
    stream = assistant_agent.run_stream(task="Get me the recipe for biryani.")
    
    await Console(stream)

    await model_client.close()
    await chroma_user_memory.close()


if __name__=="__main__":
    asyncio.run(main())



