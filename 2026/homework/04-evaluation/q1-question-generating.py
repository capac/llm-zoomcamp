from ingest import download_documents
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
documents = download_documents()
openai_client = OpenAI()

data_gen_instructions = """
You emulate a student who is taking our LLM course.
You are given one lesson page from the course.
Formulate 5 questions this student might ask that are answered by this page.

Rules:
- The page should contain the answer to each question.
- Make the questions complete and not too short.
- Use as few words as possible from the page; don't copy its phrasing.
- The questions should resemble how people actually ask things online:
  not too formal, not too short, not too long.
- Ask about the content of the lesson, not about its formatting or filename.
""".strip()


class Questions(BaseModel):
    questions: list[str]


user_prompt = json.dumps(documents[0])

messages = [
  {"role": "developer", "content": data_gen_instructions},
  {"role": "user", "content": user_prompt},
  ]

response = openai_client.responses.parse(
    model="gpt-5.4-mini",
    input=messages,
    text_format=Questions
)

if __name__ == "__main__":
    print(response.output_parsed.questions)
