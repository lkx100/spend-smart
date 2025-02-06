from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
import os

data_system_prompt = """
    Strictly Instruction: 
    1. If relevent transaction data is found, extract it without giving any extra chat messages, else don't replay.
    2. Extraction data very consistentantly with all lowercase.

    Follow the structure of the transaction data as shown in the example:
    Example:
    {
        'date': 'dd-mm-yyyy',
        'name': 'something relevent to extracted data',
        'expense': 500,
        'category': 'Grocery',
        'tag': 'tag_name'
    }
"""

class LoadTransactions():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def filter_extract(self, file_path):
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
        file_content = file_bytes.decode('utf-8', errors='ignore')
        # print(file_content)
        response = self.client.models.generate_content(
            model='gemini-2.0-flash-lite-preview-02-05',
            contents=[file_content],
            config=types.GenerateContentConfig(
                system_instruction=data_system_prompt,
                temperature=0.1
            )
        )
        print(response.text)
