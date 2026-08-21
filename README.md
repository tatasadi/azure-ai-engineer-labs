# Azure AI Engineer Labs

Python exercises I build while preparing for the Microsoft **Azure AI Engineer
Associate (AI-103)** certification. Each Microsoft Learn module becomes one or
more small, standalone Python scripts in `src/`, each named for what it
demonstrates.

> Status: active study project. These are learning-focused reference scripts for
> exam preparation, not production systems.

## Structure

markdown
azure-ai-engineer-labs/
├─ requirements.txt # shared dependencies
├─ .env.example # copy to .env and fill in
└─ src/ # one script per exercise

## Prerequisites

- Azure subscription with a Microsoft Foundry project and a deployed chat model
- Foundry User role on the project, and `az login` for local Entra ID auth
- Python 3.10+

## Setup

```
python -m venv .venv

activate: .venv\Scripts\activate (Windows) or source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # then fill in your values
```

## Run an exercise

```
python src/foundry_sdk_hello_response.py
```

## Configuration

Scripts read config from `.env` (never committed):

| Env var                 | Purpose                                |
| ----------------------- | -------------------------------------- |
| `PROJECT_ENDPOINT`      | Foundry project endpoint (Foundry SDK) |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint (OpenAI SDK)     |
| `MODEL_DEPLOYMENT`      | Deployed chat model name               |
| `AZURE_OPENAI_API_KEY`  | Optional; only for API-key auth        |

## Notes

Authentication prefers Microsoft Entra ID via `DefaultAzureCredential`. Secrets
are never committed.
