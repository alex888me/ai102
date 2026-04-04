import os
from pathlib import Path
from playsound3 import playsound
from dotenv import load_dotenv

# Import namespaces
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def main():
    try:
        endpoint=os.getenv("MODEL_ENDPOINT_TTS_Target_URI")
        model_deployment=os.getenv("MODEL_NAME_TTS")
        speech_file_path = Path(__file__).parent / "speech_tts.mp3"


        # Create the Azure OpenAI client
        token_provider = get_bearer_token_provider(                    
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider = token_provider,
            api_version="2025-03-01-preview"
        )

        # Generate speech and save to file
        with client.audio.speech.with_streaming_response.create(
                    model=model_deployment,
                    voice="alloy",
                    input="My voice is my passport!",
                    instructions="Speak in a serious tone.",
                ) as response:
            response.stream_to_file(speech_file_path)


        # Play the generated speech file
        playsound(speech_file_path)

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main() 
