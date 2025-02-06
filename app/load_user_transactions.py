from google import genai
from google.genai import types
from pypdf import PdfReader
from dotenv import load_dotenv
import json
load_dotenv()
import os

data_system_prompt = """
    Strictly Instruction: 
    1. If relevent transaction data is found, extract it without giving any extra chat messages, else don't replay.
    2. Extraction data very consistentantly with all lowercase.

    Follow the structure of the transaction data as shown in the example:
    Example:
    [
        {
            'date': 'dd-mm-yyyy',
            'name': 'something relevent to extracted data',
            'expense': 500,
            'category': 'Grocery',
            'tag': 'tag_name'
        },
        {
            'date': 'dd-mm-yyyy',
            'name': 'something relevent to extracted data',
            'expense': 500,
            'category': 'Grocery',
            'tag': 'tag_name'
        },
        so on ...
    ]
"""

class LoadTransactions():
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # def clean_transaction(self, transaction):
    #     """Clean and validate a single transaction"""
    #     return {
    #         'date': transaction.get('date', ''),
    #         'name': transaction.get('name', '').lower(),
    #         'expense': float(transaction.get('expense', 0)),
    #         'category': transaction.get('category', '').lower(),
    #         'tag': transaction.get('tag')
    #     }

    def filter_extract(self, file_path):
        try:
            # with open(file_path, 'rb') as file:
            #     file_bytes = file.read()
            # file_content = file_bytes.decode('utf-8', errors='ignore')
            # print(file_content)

            pdf_reader = PdfReader(file_path)
            text_content = ""

            for page in pdf_reader.pages:
                text_content += page.extract_text()

            prompt = f"""
                {data_system_prompt}

                Extract transaction data from the following bank statement:
                {text_content}

                Return the data in valid JSON format with double quotes.
            """

            response = self.client.models.generate_content(
                model='gemini-2.0-flash-lite-preview-02-05',
                contents=[prompt],
                config=types.GenerateContentConfig(
                    temperature=0.1
                )
            )
            transactions = response.text[7:-3]
            # print(transactions)
            # print(type(transactions), "Length:", len(transactions))

        
            try:
                transactions = json.loads(transactions)
                # print(transactions)
                # print(type(transactions), "Length:", len(transactions))
                return transactions
            #     # Validate and clean each transaction
            except Exception as e:
                print(f"Error parsing transactions: {str(e)}")
                return None  

        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return None
