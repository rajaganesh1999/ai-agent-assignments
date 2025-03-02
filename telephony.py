# from twilio.rest import Client
# from dotenv import load_dotenv
# import os

# load_dotenv()

# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# def start_call(to_number):
#     call = client.calls.create(
#         to=to_number,
#         from_=TWILIO_PHONE_NUMBER,
#         twiml="<Response><Say>Hello! This is your AI assistant.</Say></Response>"
#     )
#     return call.sid


from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def start_call(to_number):
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_PHONE_NUMBER,
        twiml="<Response><Say>Hello! This is your AI assistant.</Say></Response>"
    )
    return call.sid

def handle_incoming_call():
    """Handles incoming calls and responds to the caller."""
    response = VoiceResponse()
    response.say("Hello! This is your AI assistant. How can I help you today?")
    response.record(max_length=10, play_beep=True, action="/process-recording")
    return str(response)
