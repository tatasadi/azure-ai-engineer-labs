import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

load_dotenv()
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment_name = os.environ["MODEL_DEPLOYMENT"]

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(base_url=azure_openai_endpoint, api_key=token_provider())
response = client.responses.create(
  model=deployment_name,
  input="Hello, who are you?"
)

print(f"response output: {response.output_text}")

