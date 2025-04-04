# 1. Import our agent class
from autogen import ConversableAgent, LLMConfig

# 2. Define our LLM configuration for OpenAI's GPT-4o mini
#    uses the OPENAI_API_KEY environment variable
llm_config = LLMConfig(api_type="openai", model="gpt-4o-mini")
with llm_config:
    my_agent = ConversableAgent(
        name="helpful_agent",
        system_message="You are a poetic AI assistant, respond in rhyme.",
    )

def chat():
    prompt=str(input("What do you want to know?"))
    # 4. Run the agent with a prompt
    if(prompt!="exit"):
        chat_result = my_agent.run(prompt)

        # 5. Print the chat
        print(chat_result.chat_history)
    else:
        return False


if __name__=="__main__":
    chat()
 