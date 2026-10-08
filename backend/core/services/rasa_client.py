import os
import requests

RASA_URL = os.getenv("RASA_URL", "http://localhost:5005")

def send_message(sender: str, message: str):
    response = requests.post(
        f"{RASA_URL}/webhooks/rest/webhook",
        json={
            "sender": sender,
            "message": message,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()