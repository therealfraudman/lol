from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

@app.route("/sms", methods=["POST"])
def sms_webhook():
    data = request.get_json()
    try:
        from_number = data['data']['payload']['from']['phone_number']
        to_number = data['data']['payload']['to'][0]['phone_number']
        text = data['data']['payload']['text']
        send_to_telegram(f"📩 SMS Received\nFrom: {from_number}\nTo: {to_number}\n\n{text}")
    except Exception as e:
        send_to_telegram(f"⚠️ Error parsing SMS: {str(e)}")
    return "OK", 200
