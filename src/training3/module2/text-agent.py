import os
from pathlib import Path

from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


def main():
    try:
        project_endpoint = os.getenv("PROJECT_ENDPOINT")
        agent_name = os.getenv("AGENT_NAME")

        with (
            DefaultAzureCredential() as credential,
            AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
            project_client.get_openai_client() as openai_client,
        ):
            prompt = input("User prompt: ")
            response = openai_client.responses.create(
                input=[{"role": "user", "content": prompt}],
                extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
            )

        print(f"{agent_name}: {response.output_text}")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
