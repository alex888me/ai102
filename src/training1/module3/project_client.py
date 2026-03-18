import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

az_credential=DefaultAzureCredential()
token = az_credential.get_token("https://management.azure.com/.default")
project_client = AIProjectClient(
    credential=az_credential,
    endpoint=os.environ["PROJECT_ENDPOINT"]
)

print("Got token:", token.token[:20], "...")
