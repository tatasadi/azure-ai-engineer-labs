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

function_tools = [
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
        instructions="You are an AI assistant that provides information.",
        tools=function_tools,
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
                tools=function_tools,
                previous_response_id=last_response_id
            )
            last_response_id = response.id

    print(response.output_text)





