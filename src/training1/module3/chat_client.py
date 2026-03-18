import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


# Get project client
project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["PROJECT_ENDPOINT"]
)
    
# Get a chat client
chat_client = project_client.get_openai_client()

# Get a chat completion based on a user-provided prompt
user_prompt = input("Enter a question:")

response = chat_client.chat.completions.create(
    model='gpt-4.1-mini',
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": user_prompt}
    ]
)
print(response.choices[0].message.content)
