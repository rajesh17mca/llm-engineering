from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai = OpenAI()

def talker(message):
    response = openai.audio.speech.create(
      model="tts-1",
      voice="onyx",    # Also, try replacing onyx with alloy
      input=message
    )
    
    audio_stream = BytesIO(response.content)
    audio = AudioSegment.from_file(audio_stream, format="mp3")
    play(audio)

talker("Well, hi there")