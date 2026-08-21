import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment_name = os.environ["MODEL_DEPLOYMENT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]


client = OpenAI(base_url=azure_openai_endpoint, api_key=api_key)
response = client.responses.create(
  model=deployment_name,
  input="Hello, who are you?"
)

print(f"response output: {response.output_text}")

