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

def get_order_status(orderid):
    return f"Order {orderid} shipped on 2026-08-24 and arrives Friday."

function_tools = [
    {
        "type": "function",
        "name": "get_time",
        "description": "Get the current time"
    },
    {
        "type": "function",
        "name": "get_order_status",
        "description": "Get the delivery status of a customer order by its order ID",
        "parameters": {
            "type": "object",
            "properties": {
                "orderid": {
                    "type": "string",
                    "description": "The order ID, for example 'ORD-1234'"
                }
            },
            "required": ["orderid"],
            "additionalProperties": False
        }
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

    tool_outputs = []
    for item in response.output:
        if item.type != "function_call":
            continue

        args = json.loads(item.arguments)

        if item.name == "get_time":
            result = get_time()
        elif item.name == "get_order_status":
            result = get_order_status(args["orderid"])
        else:
            result = f"Unknown function: {item.name}"

        tool_outputs.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": result
        })

    if tool_outputs:
        response = client.responses.create(
            model=deployment_name,
            instructions="Answer using the tool output",
            input=tool_outputs,
            tools=function_tools,
            previous_response_id=last_response_id
        )
        last_response_id = response.id

    print(response.output_text)





