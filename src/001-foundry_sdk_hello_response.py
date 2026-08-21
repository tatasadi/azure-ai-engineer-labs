import os
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

load_dotenv()
project_endpoint = os.environ["PROJECT_ENDPOINT"]
deployment_name = os.environ["MODEL_DEPLOYMENT"]

project = AIProjectClient(
  endpoint=project_endpoint,
  credential=DefaultAzureCredential()
)
client = project.get_openai_client()
response = client.responses.create(
  model=deployment_name,
  input="Hello, who are you?"
)

print(f"response output: {response.output_text}")

