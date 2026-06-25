import os
from dotenv import load_dotenv
from ingest import download_documents
from minsearch import Index
from openai import OpenAI
from rag_helper import RAGBase, INSTRUCTIONS, PROMPT_TEMPLATE

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

index = Index(
    text_fields=["content"],
    keyword_fields=["filename"]
)

documents = download_documents()
index.fit(documents)
print("Indexing completed.")

question = "How does the agentic loop keep calling the model until it stops?"

rag = RAGBase(
    index=index,
    llm_client=openai_client,
    instructions=INSTRUCTIONS,
    prompt_template=PROMPT_TEMPLATE,
)

print(f"Question: {question}")
assistant = rag.rag_query(question)
print(f"Number of input tokens: {assistant.usage.input_tokens}")
