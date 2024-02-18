from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from google.generativeai import GenerativeModel, configure

configure(api_key=os.environ["GEMINI_API_KEY"])

model = GenerativeModel('gemini-pro')


def ask_gemini_api(question):
    chat = model.start_chat()
    response = chat.send_message(question)
    return response.text
