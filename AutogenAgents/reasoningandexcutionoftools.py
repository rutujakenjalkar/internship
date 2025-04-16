import random
from typing import Annotated
from autogen import ConversableAgent, UserProxyAgent,register_function,LLMConfig
from autogen.agents.experimental import ReasoningAgent
from pydantic import BaseModel 


api_key=""

verbose=True

random.seed(1)

llm_config=LLMConfig(api_type="openai",model="gpt-4o-mini",api_key=api_key)



def WelcomeTool(name:Annotated[str,"Name of the person"])->str:
    return f"WELCOME ABOARD {name}."


message_to_thinker="""You are a reasoning agent which helps user solve their tasks by selecting the most appropriate tools and its arguments to solve the task .
You will be given only some tools you have to chosen one of them to solve the task.You should respond by calling the correct tool with its arguments using function calls, not plain text.

the tools are :
1.WelcomeTool:To Welcome a particular user
  Arugments of the Welcome Tool: name

Example:
User Query: Welcome John Doe
Response: Call the WelcomeTool with name="John Doe"
"""






async def last_meaningful_msg(sender, recipient, summary_args):
    import warnings

    if sender == recipient:
        return "TERMINATE"

    summary = ""
    chat_messages = recipient.chat_messages[sender]

    for msg in reversed(chat_messages):
        try:
            content = msg["content"]
            if isinstance(content, str):
                summary = content.replace("TERMINATE", "")
            elif isinstance(content, list):
                # Remove the `TERMINATE` word in the content list.
                summary = "\n".join(
                    x["text"].replace("TERMINATE", "") for x in content if isinstance(x, dict) and "text" in x
                )
            if summary:
                return summary
        except (IndexError, AttributeError) as e:
            warnings.warn(f"Cannot extract summary using last_msg: {e}. Using an empty str as summary.", UserWarning)
    return summary




with llm_config:
    reason_agent=ReasoningAgent(
        name="reason_agent",
        system_message=message_to_thinker,
        reason_config={"method":"mcts","nsim":1,"max_depth":2}

    )

    executor_agent = ConversableAgent(
        name="executor_agent",
        human_input_mode="NEVER",
    )


register_function(
    WelcomeTool,
    caller=executor_agent,
    executor=executor_agent,
    description="Welcome a user by name",
)



ans = reason_agent.initiate_chat(recipient=executor_agent, message="""With the tools given to you please welcome the user - "Rutuja Kenjalkar""", max_turns=2)

print(ans.chat_history[-1]["content"])