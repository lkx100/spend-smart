import requests
from dotenv import load_dotenv
load_dotenv()
import os

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "57589685-8200-4a11-909d-4003f17b061b"
FLOW_ID = "2703f5ea-8405-445c-9423-ddce28c0afa6"
APPLICATION_TOKEN = os.getenv("ASTRA_KEY")
ENDPOINT = FLOW_ID 

def run_flow(message) -> dict:

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if APPLICATION_TOKEN:
        # print(APPLICATION_TOKEN)
        headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
        response = requests.post(api_url, json=payload, headers=headers)
        response_json = response.json()
        print("Response json:", response_json)
        
        # Extract only the text from the nested response
        response_text = response_json['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        # print(response.json(), response_text)
        return {"response": response_text}
    else:
        print(f"No API KEY found")

