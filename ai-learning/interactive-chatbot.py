import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

openai = OpenAI()
MODEL = 'gpt-4o-mini'
system_message = "You are a helpful assistant"

def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response

gr.ChatInterface(fn=chat, type="messages").launch()
