from dotenv import load_dotenv
import os

# import namespaces
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

def main():
    try:
        project_endpoint = os.getenv("PROJECT_ENDPOINT") or os.getenv("FOUNDRY_ENDPOINT")
        agent_name = os.getenv("AGENT_NAME")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        if not project_endpoint:
            raise ValueError("Missing PROJECT_ENDPOINT (or FOUNDRY_ENDPOINT).")
        if not agent_name:
            raise ValueError("Missing AGENT_NAME.")
        if not model_deployment:
            raise ValueError("Missing model deployment. Set MODEL_NAME, MODEL_DEPLOYMENT, or MODEL_DEPLOYMENT_NAME.")

        # Get project client
        project_client = AIProjectClient(
            endpoint=project_endpoint,
            credential=DefaultAzureCredential(),
        )
                
        # Get an OpenAI client
        openai_client = project_client.get_openai_client()
        
        # Main loop
        while True:
            # Get user input
            prompt = input("User prompt (or 'quit'): ")
            if prompt == "quit" or len(prompt) == 0:
                break
            else:
                # Use the agent to get a response
                response = openai_client.responses.create(
                    model=model_deployment,
                    input=[{"role": "user", "content": prompt}],
                    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
                )

                print(f"{agent_name}: {response.output_text}")
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
