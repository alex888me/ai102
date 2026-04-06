from dotenv import load_dotenv
import os
import json
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential
from pathlib import Path


def main():
    try:
        # Get the business card schema
        json_file = Path(__file__).resolve().parent.joinpath('biz-card.json')
        with open(json_file, "r") as file:
            schema_json = json.load(file)
        
        card_schema = json.dumps(schema_json)

        # Get config settings
        ai_svc_endpoint = os.getenv('RECOURCE_ENDPOINT')
        ai_svc_key = os.getenv('API_KEY')
        analyzer = os.getenv('ANALYZER')

        # Create the analyzer
        create_analyzer (card_schema, analyzer, ai_svc_endpoint, ai_svc_key)

        print("\n")

    except Exception as ex:
        print(ex)



def create_analyzer (schema, analyzer, endpoint, key):
    # Create a Content Understanding analyzer
    print(f"Creating {analyzer}")
    print(f"Endpoint: {endpoint}")

    # Create the Content Understanding client
    client = ContentUnderstandingClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Parse the schema JSON into a ContentAnalyzer object
    analyzer_definition = json.loads(schema)

    # Create the analyzer using the SDK (long-running operation)
    poller = client.begin_create_analyzer(
        analyzer_id=analyzer,
        resource=analyzer_definition,
        allow_replace=True
    )

    # Wait for the operation to complete
    result = poller.result()
    print(f"Analyzer '{analyzer}' created successfully.")
    print(f"Status: {result['status'] if isinstance(result, dict) else 'Succeeded'}")

    # Read the analyzer back from the service so we can confirm it exists
    created_analyzer = client.get_analyzer(analyzer)
    print(f"Verified analyzer from service: {created_analyzer.analyzer_id}")
    print(f"Analyzer state: {created_analyzer.status}")


if __name__ == "__main__":
    main()        
