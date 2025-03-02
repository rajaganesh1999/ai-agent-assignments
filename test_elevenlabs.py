import requests
import os
from dotenv import load_dotenv
import pytest

load_dotenv()  # Load environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"

headers = {
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
}

data = {
    "text": "Hello! This is an AI-generated voice test.",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
}

def test_elevenlabs_tts():
    response = requests.post(url, headers=headers, json=data)
    assert response.status_code == 200, f"Error: {response.status_code} - {response.text}"
    # Save the response as an audio file
    with open("output_audio.mp3", "wb") as f:
        f.write(response.content)
    print("AI-generated voice saved as 'output_audio.mp3'")
