import os
from dotenv import load_dotenv
from ingest import download_documents, index_documents
from openai import OpenAI
from rag_helper import RAGBase

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

documents = download_documents()
index = index_documents(documents)
print("Indexing completed.")

question = "How does the agentic loop keep calling the model until it stops?"

INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()


rag = RAGBase(
    index=index,
    llm_client=openai_client,
    instructions=INSTRUCTIONS,
    prompt_template=PROMPT_TEMPLATE,
)

print(f"Question: {question}")
assistant = rag.rag_query(question)
print(f"Number of input tokens: {assistant.usage.input_tokens}")
