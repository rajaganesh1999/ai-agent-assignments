import requests
import json
from dotenv import load_dotenv
import os
import pytest

load_dotenv()  # Load environment variables
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if DEEPGRAM_API_KEY is None:
    raise ValueError("DEEPGRAM_API_KEY is not set. Please check your environment variables.")


# Use any sample audio file (replace with your file)
AUDIO_FILE = "sample_audio.wav"

url = "https://api.deepgram.com/v1/listen"
headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "audio/wav"
}

def test_deepgram_transcription():
    print("Transcription successful:", response.json())
