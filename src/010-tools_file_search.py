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

vector_store = client.vector_stores.create(name="policy_docs")
client.vector_stores.files.upload(
    vector_store_id=vector_store.id,
    file=open("data/expenses_policy.txt", "rb")
)

response = client.responses.create(
    model=deployment_name,
    instructions="You are an AI assistant that provides information from HR policy documents.",
    input="What's the max I can claim for a taxi?",
    tools=[{
        "type":"file_search",
        "vector_store_ids": [vector_store.id]
    }],
    include=["file_search_call.results"]
)

print(f"response output text: {response.output_text}")

