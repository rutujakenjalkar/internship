
from autogen import LLMConfig
from autogen.agents.experimental import DocAgent, InMemoryQueryEngine


llm_list =  LLMConfig(api_type="openai", model="gpt-4o-mini")
llm_config=llm_list

llm_config_dict = {
    "api_type": "openai",
    "model": "gpt-4o-mini",
   
}
# Create our In-Memory Query Engine
inmemory_qe = InMemoryQueryEngine(llm_config_dict)

# Include the Query Engine when creating your DocAgent
with llm_config:
    doc_agent = DocAgent(
        name="doc_agent",
        query_engine=inmemory_qe,
    )

# Update this path to suit your environment
doc_agent.run(
    "Can you ingest C:\\Users\\Abhay\\Documents\\internimage\\ag2\\financial_report_q1_2025.pdf and tell me the Q1 2025 financial summary?",
    max_turns=1
)