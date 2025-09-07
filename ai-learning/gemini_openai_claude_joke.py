import os, requests, json
import google.generativeai
import anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'key not available')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'key not available')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

openai = OpenAI()
anthropicai = anthropic.Anthropic()
google.generativeai.configure()

system_message = "You are an assistent that is great at telling jokes"
user_prompt = "Tell a light-hearted joke for an audience of DevOps engineers"

prompts = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': user_prompt}
]

def openai_model():
    completions = openai.chat.completions.create(
        model='gpt-4o-mini', messages=prompts
    )
    print(completions.choices[0].message.content)

def gemini_model():
    gemini = google.generativeai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_message
    )
    response = gemini.generate_content(user_prompt)
    print(response.text)

def anthropic_model():
    completion = anthropicai.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=200,
        temperature=0.7,
        system=system_message,
        messages=[
            {'role': 'user', 'content': user_prompt}
        ]
    )
    print(completion.content[0].text)

def anthropic_model_stream():
    result = anthropicai.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=200,
        temperature=0.7,
        system=system_message,
        messages=[
            {'role': 'user', 'content': user_prompt}
        ]
    )
    
    with result as stream:
        for text in stream.text_stream:
            print(text, end='', flush=True)

if __name__ == "__main__":
    openai_model()
    anthropic_model()
    anthropic_model_stream()
    gemini_model()