import os

from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Create client using endpoint and key
credential = DefaultAzureCredential()
client = TextAnalyticsClient(
    endpoint=os.environ["RECOURCE_ENDPOINT"], 
    credential=credential,
)

documents = ["John Smith works at Contoso Ltd. His email is john.smith@contoso.com and his phone number is 555-012-456.",
             "Patient Sarah Johnson, SSN 123-45-6789, was admitted on 03/15/2024."]

# Extract PII entities
response = client.recognize_pii_entities(documents=documents, language="en")
for doc in response:
    print(f"\nPII entities in document {doc.id}:")
    for entity in doc.entities:
        print(f" - {entity.text}: {entity.category} (confidence: {entity.confidence_score:.2f})")

    print()
    print(f"\nDocument {doc.id} (redacted):")
    print(f" {doc.redacted_text}")