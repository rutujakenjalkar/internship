# 🧠 Conversable Agent

The **Conversable Agent** is the most basic fully functional agent provided by the [AutoGen](https://github.com/microsoft/autogen) framework. It enables natural language interactions with users and forms the superclass for other agent types.

It can carry on a conversation until a termination message is explicitly given, making it a foundation for building more complex agents.

---

## ✨ Key Features

- Simple, intuitive conversation handling with the user.
- Acts as a base class for other agents.
- Remains active until a termination message is received.
- Can be easily configured using LLM settings.

---


## 🛠️ Steps to Create a Conversable Agent

Here’s how to build one:

1. **Import Required Classes**  
   Import `ConversableAgent` and `LLMConfig` from the `autogen` framework.

2. **Create the LLM Configuration**  
   Set up the LLM using the following parameters:
   - `api_type` (e.g., `"openai"`)
   - `model` (e.g., `"gpt-4"` or `"gpt-3.5-turbo"`)
   - `api_key` (your secure OpenAI key)

3. **Instantiate the Agent**  
   Create the `ConversableAgent` object and pass a custom system message to describe the agent's role and behavior.

4. **Run the Agent**  
   Start the interaction by sending a prompt.  
   The agent will continue the conversation until it receives a termination message.

---

## 🧪 Example

```python
from autogen import ConversableAgent, LLMConfig

llm_config = LLMConfig(
    api_type="openai",
    api_key="your-api-key-here",
    model="gpt-4"
)

agent = ConversableAgent(
    name="HelperAgent",
    llm_config=llm_config,
    system_message="You are a helpful assistant that provides accurate information."
)

agent.run()
