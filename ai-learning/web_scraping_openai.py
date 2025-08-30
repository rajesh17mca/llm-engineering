import os 
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Markdown, display


class Summarize:
    load_dotenv()

    def __init__(self, url):
        self.url = url
        resp = self.get_webpage(url)
        if resp is not None:
            soup = BeautifulSoup(resp.content, 'html.parser')
            self.title = soup.title.string if soup.title else "Not Found"
            for irrelevent in soup.body(['script', 'style', 'img', 'input']):
                irrelevent.decompose()
            self.text = soup.body.get_text(separator='\n', strip=True)
        else:
            self.text = "Sorry Response object has some issue"
        self.generate_summary(self.text, self.title)

    def get_webpage(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp
        else:
            return None
    
    def generate_summary(self, text, title):
        system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in English."
        user_prompt = self.get_uster_prompt(text, title)
        ai_resp = self.get_resp_from_openai(system_prompt, user_prompt)
        print(ai_resp)

    def get_uster_prompt(self, text, title):
        user_prompt = f"You are looking at a website titled {title}"
        user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n"
        user_prompt += text
        return user_prompt
        
    def get_resp_from_openai(self, system_prompt, user_prompt):
        openai = OpenAI()
        messages = [
            {'role': 'system', 'content':system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        openai_resp = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages
        )
        return openai_resp.choices[0].message.content
        
Summarize("https://www.python.org/")
# Summarize("https://www.google.com/")
