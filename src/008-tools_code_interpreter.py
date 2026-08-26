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
    instructions="You are an assistant. Use python tool for calculations",
    input="What is the standard deviation of [12, 7, 22, 5, 18]?",
    tools=[{"type":"code_interpreter", "container": {"type": "auto"}}]
)

print(f"response output: {response.output}")
print(f"response output text: {response.output_text}")

