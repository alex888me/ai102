import os

from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Create client using endpoint and key
credential = DefaultAzureCredential()
client = TextAnalyticsClient(
    endpoint=os.environ["RECOURCE_ENDPOINT"], 
    credential=credential,
)

documents = ["Hello World!", "Bonjour le monde!"]

response = client.detect_language(documents=documents)
for doc in response:
    print(f"Document: {doc.id}")
    print(f"\tPrimary Language: {doc.primary_language.name}")
    print(f"\tISO6391 Name: {doc.primary_language.iso6391_name}")
    print(f"\tConfidence Score: {doc.primary_language.confidence_score}")