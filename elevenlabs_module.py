import requests
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech(text):
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech",
        headers=headers,
        json={"text": text, "voice_id": "YOUR_VOICE_ID"}
    )
    return response.json()["audio_url"]
