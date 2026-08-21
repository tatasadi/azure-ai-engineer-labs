import asyncio
import os

from dotenv import load_dotenv
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import DefaultAzureCredential

INSTRUCTIONS = "you are a useful travel assistant, answer only the questions about traveling."


async def main():
    load_dotenv()
    project_endpoint = os.environ["PROJECT_ENDPOINT"]
    deployment_name = os.environ["MODEL_DEPLOYMENT"]

    async with DefaultAzureCredential() as credential, \
               AIProjectClient(endpoint=project_endpoint, credential=credential) as project:
        client = project.get_openai_client()

        print('ask a question or type "quit" to quit')
        last_response_id = None

        while True:
            user_input = await asyncio.to_thread(input)

            if user_input == "quit":
                break

            stream = await client.responses.create(
                model=deployment_name,
                input=user_input,
                instructions=INSTRUCTIONS,
                stream=True,
                previous_response_id=last_response_id,
            )

            async for event in stream:
                if event.type == "response.output_text.delta":
                    print(event.delta, end="", flush=True)
                elif event.type == "response.completed":
                    last_response_id = event.response.id

            print()


asyncio.run(main())
