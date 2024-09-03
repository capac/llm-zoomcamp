from openai import OpenAI
import os
import json

api_token_key = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=api_token_key)
query = "What's the formula for energy?"

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{"role": "user", "content": query}],
    temperature=0.0,
)

completion_tokens = json.loads(response.json())['usage']['completion_tokens']
print(f"Number of completion tokens: {completion_tokens}")
