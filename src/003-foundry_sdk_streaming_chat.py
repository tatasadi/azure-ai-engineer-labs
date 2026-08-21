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

print("ask a question or type \"quit\" to quit")

last_response_id = None

while True:
    user_input = input()

    if user_input == "quit":
        break

    stream = client.responses.create(
        model=deployment_name,
        input=user_input,
        instructions="you are a useful travel assistant, answer only the questions about traveling.",
        stream=True,
        previous_response_id=last_response_id
    )

    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
        elif event.type == "response.completed":
            last_response_id = event.response.id

    print()


