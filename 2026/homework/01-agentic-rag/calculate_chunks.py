import os
from dotenv import load_dotenv
from gitsource import GithubRepositoryDataReader, chunk_documents
from openai import OpenAI
from minsearch import Index
from rag_helper import RAGBase, INSTRUCTIONS, PROMPT_TEMPLATE


load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id="8c1834d",
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)

print("Downloading lessons...")
files = reader.read()

documents = []

for file in files:
    doc = file.parse()
    documents.append(doc)

chunks = chunk_documents(documents, size=2000, step=1000)

print(f"Number of chunks created: {len(chunks)}")

index = Index(
    text_fields=["content"],
    keyword_fields=["filename"]
)

index.fit(chunks)
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
