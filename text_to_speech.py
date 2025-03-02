import elevenlabs
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech(text):
    audio = elevenlabs.generate(text, api_key=ELEVENLABS_API_KEY)
    return audio
