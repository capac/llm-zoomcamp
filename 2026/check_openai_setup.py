from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.com/openai/v1"
)

try:
    openai_client.responses
    print("OpenAI setup check completed.")
except Exception as e:
    print(f"Error occurred while setting up OpenAI: {e}")
