import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/v1"
)

try:
    response = openai_client.responses.create(
        model="gpt-5-mini",
        input="What is the weather like today in London, UK?"
        )
    print(response.output_text)
except Exception as e:
    print(f"Error occurred while setting up OpenAI: {e}")
