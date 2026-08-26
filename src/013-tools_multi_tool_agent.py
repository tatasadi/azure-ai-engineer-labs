import json
import time
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

def get_time():
    return f"The time is {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"

vector_store = client.vector_stores.create(name="policy_docs")
client.vector_stores.files.upload(
    vector_store_id=vector_store.id,
    file=open("data/expenses_policy.txt", "rb")
)

tools = [
    {
        "type": "code_interpreter",
        "container":
        {
            "type": "auto"
        }
    },
    {
        "type": "web_search"
    },
    {
        "type": "file_search",
        "vector_store_ids": [vector_store.id]
    },
    {
        "type": "function",
        "name": "get_time",
        "description": "Get the current time"
    }
]

last_response_id = None

while True:
    user_input = input("Ask a question or type \"quit\" to exit: ")
    if user_input.lower() == "quit":
        break

    response = client.responses.create(
        model=deployment_name,
        instructions="You are an AI assistant that provides information. Use python tool for calculations. use web search when current info is required and prefer reputable sources. You can also provide information from HR policy documents",
        tools=tools,
        input=user_input,
        previous_response_id=last_response_id
    )
    last_response_id = response.id

    for item in response.output:
        if item.type == "function_call" and item.name == "get_time":
            current_time = get_time()
            response = client.responses.create(
                model=deployment_name,
                instructions="Answer only with the tool output",
                input=[{
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": current_time
                }],
                tools=tools,
                previous_response_id=last_response_id
            )
            last_response_id = response.id

    print(response.output_text)





