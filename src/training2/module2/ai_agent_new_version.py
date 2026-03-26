"""Microsoft Foundry SDKs and Endpoints
https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview?pivots=programming-language-python
"""

import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai import OpenAI


### Using the OpenAI SDK ###
openai_client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["API_KEY"],
)

response = openai_client.responses.create(
    model="gpt-4.1",
    input= "What is the size of France in square miles?" 
)

print(response.model_dump_json(indent=2)) 
