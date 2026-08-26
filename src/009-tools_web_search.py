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
    instructions="You are a helpful assistant. use web search when current info is required and prefer reputable sources.",
    input="What are the latest Azure OpenAI model announcements this month?",
    tools=[{"type":"web_search"}]
)

print(f"response output text: {response.output_text}")

