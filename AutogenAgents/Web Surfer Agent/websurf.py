# 1. Import our WebSurferAgent
from autogen import LLMConfig
from autogen.agents.experimental import WebSurferAgent


# Put your key in the OPENAI_API_KEY environment variable
llm_config = LLMConfig(api_type="openai", model="gpt-4o-mini")

# 2. Add additional browser configurations for our browser-use tool
browser_use_browser_config = {"browser_config": {"headless": False}, "agent_kwargs": {"generate_gif": True}}

# 3. Create the agent, nominating the tool and tool config
with llm_config:
    web_researcher = WebSurferAgent(
        name="researcher",
        web_tool="browser_use",
        web_tool_kwargs=browser_use_browser_config,
    )

# 4. Run our agent, passing in the tools that our WebSurferAgent has so they can be executed
ag2_news_result = web_researcher.run(
    "Search for the latest news on IPL ",
    tools=web_researcher.tools,
)

print(ag2_news_result.summary)