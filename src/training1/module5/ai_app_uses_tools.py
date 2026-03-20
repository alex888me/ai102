"""https://microsoftlearning.github.io/mslearn-ai-studio/Instructions/Exercises/04a-use-own-data.html"""

import os
import glob
from dotenv import load_dotenv
from openai import OpenAI


VECTOR_STORE_NAME = "travel-brochures"


def get_vector_store_by_name(openai_client, name):
    page = openai_client.vector_stores.list()
    while True:
        for vector_store in page.data:
            if vector_store.name == name:
                return vector_store
        if not page.has_next_page():
            return None
        page = page.get_next_page()


def main(): 
    openai_client = OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["API_KEY"],
    )


    vector_store = get_vector_store_by_name(openai_client, VECTOR_STORE_NAME)
    if vector_store:
        print(f"Reusing existing vector store '{VECTOR_STORE_NAME}' ({vector_store.id}).")
    else:
        brochure_pattern = f'{os.environ["PATH_BROCHURES"]}/*.pdf'
        file_paths = glob.glob(brochure_pattern)
        if not file_paths:
            print("No PDF files found in the brochures folder!")
            return

        print("Creating vector store and uploading files...")
        vector_store = openai_client.vector_stores.create(name=VECTOR_STORE_NAME)
        file_streams = [open(path, "rb") for path in file_paths]
        try:
            file_batch = openai_client.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id,
                files=file_streams
            )
        finally:
            for f in file_streams:
                f.close()

        print(f"Vector store created with {file_batch.file_counts.completed} files.")


    # Track conversation state
    last_response_id = None

    # Loop until the user wants to quit
    while True:
        input_text = input('\nEnter a question (or type "quit" to exit): ')
        if input_text.lower() == "quit":
            break
        if len(input_text) == 0:
            print("Please enter a question.")
            continue

        # Get a response using tools
        response = openai_client.responses.create(
            model=os.environ["MODEL_DEPLOYMENT"],
            instructions="""
            You are a travel assistant that provides information on travel services available from Margie's Travel.
            Answer questions about services offered by Margie's Travel using the provided travel brochures.
            Search the web for general information about destinations or current travel advice.
            """,
            input=input_text,
            previous_response_id=last_response_id,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [vector_store.id]
                },
                {
                    "type": "web_search_preview"
                }
            ]
        )
        print(response.output_text)
        last_response_id = response.id

if __name__ == '__main__': 
    main()
