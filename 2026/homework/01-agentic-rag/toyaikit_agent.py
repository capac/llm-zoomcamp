from pprint import pprint
from dotenv import load_dotenv
from ingest import download_documents, index_documents
from gitsource import chunk_documents
from minsearch import Index
from toyaikit.llm import OpenAIClient
from toyaikit.tools import Tools
from toyaikit.chat import IPythonChatInterface
from toyaikit.chat.runners import (
    OpenAIResponsesRunner, DisplayingRunnerCallback
    )

load_dotenv()

documents = download_documents()
index = index_documents(documents)

chunks = chunk_documents(documents, size=2000, step=1000)

print(f"Number of chunks created: {len(chunks)}")

index = Index(
    text_fields=["content"],
    keyword_fields=["filename"]
)

index.fit(chunks)
print("Indexing completed.")


def search(query: str) -> dict[str, str]:
    """
    Search the FAQ database for entries matching the given query.
    """
    return index.search(
        query,
        num_results=5,
        boost_dict={"question": 3.0, "section": 0.5},
        # filter_dict={"course": "llm-zoomcamp"}
    )


agent_tools = Tools()
agent_tools.add_tool(search)

print(f"Show agent tools: {agent_tools.get_tools()}")

chat_interface = IPythonChatInterface()
callback = DisplayingRunnerCallback(chat_interface)

instructions = """
    You're a course teaching assistant. Answer the student's question
    using the search tool. Make multiple searches with different
    keywords before answering."""

query = """
    How does the agentic loop work, and how is it
    different from plain RAG?""".strip()

runner = OpenAIResponsesRunner(
    tools=agent_tools,
    developer_prompt=instructions,
    chat_interface=chat_interface,
    llm_client=OpenAIClient(model="gpt-5.4-mini")
)

result = runner.loop(
    prompt=query,
    callback=callback
)

print(f"Cost of result: {result.cost}\n")
pprint(f"Messages: {result.last_message}")
