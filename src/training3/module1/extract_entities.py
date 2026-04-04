import os

from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Create client using endpoint and key
credential = DefaultAzureCredential()
client = TextAnalyticsClient(
    endpoint=os.environ["RECOURCE_ENDPOINT"], 
    credential=credential,
)

documents = ["Microsoft was founded on April 4, 1975 by Bill Gates and Paul Allen in Albuquerque, New Mexico.",
             "Satya Nadella became CEO of Microsoft on February 4, 2014."]

# Extract named entities
response = client.recognize_entities(documents=documents)
for doc in response:
    print(f"Entities in document {doc.id}:")
    for entity in doc.entities:
        print(f" - {entity.text} ({entity.category})")