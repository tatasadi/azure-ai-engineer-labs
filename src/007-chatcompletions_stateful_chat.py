import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

load_dotenv()
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment_name = os.environ["MODEL_DEPLOYMENT"]

token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(base_url=azure_openai_endpoint, api_key=token_provider())

conversation_messages=[
    {
      "role": "system",
      "content": "you are a useful travel assistant, answer only the questions about traveling."
    }
]

print("Assistant: Enter a prompt (or type 'quit' to exit)")
while True:
    input_text = input("\nYou: ")
    if input_text.lower() == "quit":
        print("Assistant: Goodbye!")
        break
    conversation_messages.append({
        "role": "user",
        "content": input_text
    })

    completion = client.chat.completions.create(
        model=deployment_name,
        messages=conversation_messages
    )

    assistant_message = completion.choices[0].message.content
    print(f"\nAssistant: {assistant_message}")

    conversation_messages.append({
        "role": "assistant",
        "content": assistant_message
    })

