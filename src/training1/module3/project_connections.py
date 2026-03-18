import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Get project client
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"]
)

## List all connections in the project
connections = project_client.connections
print("List all connections:")
for connection in connections.list():
    print(f"{connection.name} ({connection.type})")

