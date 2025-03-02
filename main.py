from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks, Response
from telephony import start_call, handle_incoming_call
from conversation import process_conversation, store_conversation
from dotenv import load_dotenv
import os
import requests
import openai
from vocode.streaming.transcriber.deepgram_transcriber import DeepgramTranscriber
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizer
from vocode.streaming.models.transcriber import DeepgramTranscriberConfig
from vocode.streaming.models.synthesizer import ElevenLabsSynthesizerConfig
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

app = FastAPI()
conversation_history = {}

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Helper function to initiate the call using Twilio
def start_call(to_phone_number: str):
    try:
        # Initiate the call
        call = client.calls.create(
            to=to_phone_number,
            from_=TWILIO_PHONE_NUMBER,
            url="http://localhost:8000/outgoing-call-twiml"  # Custom TwiML URL for call instructions
        )
        return call.sid  # Return the unique SID for the call
    except Exception as e:
        raise Exception(f"Error initiating call: {str(e)}")

async def generate_response(user_input, phone_number):
    """Handles multi-turn conversation and generates a response."""
    if phone_number not in conversation_history:
        conversation_history[phone_number] = []

    conversation_history[phone_number].append({"role": "user", "content": user_input})
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4o", messages=[{"role": "system", "content": "You are a professional AI sales agent."}] + conversation_history[phone_number]
    )
    ai_response = response["choices"][0]["message"]["content"]
    conversation_history[phone_number].append({"role": "assistant", "content": ai_response})
    store_conversation(phone_number, conversation_history[phone_number])
    return ai_response

@app.get("/")
def read_root():
    return {"message": "AI Voice Agent is Running"}

@app.post("/chat/")
async def chat(user_input: str):
    """Handles normal chat functionality (from old main.py)"""
    response = process_conversation(user_input)
    return {"response": response}

@app.post("/call")
async def initiate_call_endpoint(phone_number: str):
    """Handles making an outgoing call"""
    try:
        call_sid = start_call(phone_number)
        return {"message": "Call initiated", "call_sid": call_sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/incoming-call")
async def handle_incoming_call_endpoint(phone_number: str):
    """Handles incoming calls asynchronously"""
    response = handle_incoming_call()
    return Response(content=response, media_type="application/xml")

@app.get("/outgoing-call-twiml")
def outgoing_call_twiml():
    """Provides the TwiML instructions for the outgoing call."""
    response = VoiceResponse()
    response.say("Hello, this is a test call from our AI voice agent.")
    response.pause(length=2)  # Optional: Pause before hanging up
    response.hangup()  # End the call after the message
    return Response(content=str(response), media_type="application/xml")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribes audio using Deepgram"""
    try:
        transcriber = DeepgramTranscriber(DeepgramTranscriberConfig(api_key=DEEPGRAM_API_KEY))
        transcript = transcriber.transcribe(file.file.read())
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
async def text_to_speech(text: str):
    """Converts text to speech using ElevenLabs"""
    try:
        synthesizer = ElevenLabsSynthesizer(ElevenLabsSynthesizerConfig(api_key=ELEVENLABS_API_KEY, voice="Adam"))
        audio_data = synthesizer.synthesize(text)
        return {"audio_data": audio_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond")
async def get_response(user_input: str, phone_number: str):
    """Generates a response from AI and stores conversation"""
    try:
        ai_response = await generate_response(user_input, phone_number)
        return {"response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations")
def get_conversations():
    """Fetch all stored conversations."""
    return [{"phone_number": key, "text": value} for key, value in conversation_history.items()]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
