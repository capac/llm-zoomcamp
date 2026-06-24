import os
from dotenv import load_dotenv
from gitsource import GithubRepositoryDataReader, chunk_documents
from openai import OpenAI

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
