import random

from autogen.agents.experimental import ReasoningAgent, ThinkNode
from autogen import UserProxyAgent, LLMConfig

# Put your key in the OPENAI_API_KEY environment variable
llm_config = LLMConfig(api_type="openai", model="gpt-4o-mini")

verbose = True

question = "What is the expected maximum dice value if you can roll a 6-sided dice three times?"
random.seed(1)  # setup seed for reproducibility

def last_meaningful_msg(sender, recipient, summary_args):
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
            if summary.strip().rstrip():
                return summary
        except (IndexError, AttributeError) as e:
            warnings.warn(f"Cannot extract summary using last_msg: {e}. Using an empty str as summary.", UserWarning)
    return summary

user_proxy = UserProxyAgent(
      name="user_proxy",
      human_input_mode="NEVER",
      code_execution_config=False,
      is_termination_msg=lambda x: True, # terminate when reasoning agent responds
   )
    
with llm_config:
    mcts_agent = ReasoningAgent(
        name="mcts_agent",
        system_message="answer math questions",
        # setup small depth and simulations for conciseness.
        reason_config={"method": "mcts", "nsim": 3, "max_depth": 4},
        llm_config=llm_config
    )

if __name__=="__main__":
    print("HELLO WORLD !!!!")
    ans = user_proxy.initiate_chat(mcts_agent, message=question+ " Run a python simulation to get the result", summary_method=last_meaningful_msg)

    print(ans.summary)