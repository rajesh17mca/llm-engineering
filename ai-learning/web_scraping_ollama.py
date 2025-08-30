import os, requests
from bs4 import BeautifulSoup
import ollama

class WebSummarize:
    def __init__(self, url, model):
        self.url = url
        self.model = model
        self.summarize_website(self.url)

    def summarize_website(self, url):
        resp = self.get_webpage(url)
        if resp is not None:
            soup = BeautifulSoup(resp.content, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            for irrelevent in soup.body(['script', 'style', 'img', 'input']):
                irrelevent.decompose()
            text = soup.body.get_text(separator='\n', strip=True)
        else:
            text = "Sorry Response object has some issue"

        user_message = self.prepare_user_message(title, text)

        ollama_resp = ollama.chat(model=self.model, messages=user_message)
        print(ollama_resp['message']['content'])
    
    def prepare_user_message(self, title, text):
        user_prompt = f"You are looking at a website titled {title}"
        user_prompt += "\nThe contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n"
        user_prompt += text
        
        return [
            {'role': 'user', 'content': user_prompt}
        ]

    def get_webpage(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp
        else:
            return None

MODEL = "llama3.2"

WebSummarize("https://www.python.org/", MODEL)