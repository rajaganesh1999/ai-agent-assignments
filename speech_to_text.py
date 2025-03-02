import requests
import os

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def transcribe_audio(audio_url):
    headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
    response = requests.post(
        "https://api.deepgram.com/v1/listen",
        headers=headers,
        json={"url": audio_url}
    )
    return response.json().get("transcript", "")
