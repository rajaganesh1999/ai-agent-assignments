import requests
import pytest

url = "http://127.0.0.1:8000/call"
params = {"phone_number": "+919391228911"}

def test_call_initiation():
    response = requests.post(url, params=params)
    assert response.status_code == 200, f"Error: {response.status_code} - {response.text}. Please check if the server is running and the URL is correct."

    print("Call initiated successfully:", response.json())

