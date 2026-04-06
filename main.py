from flask import Flask, request, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "token_rahasia_123")
ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "active",
        "message": "WhatsApp Webhook is running!",
        "endpoints": {
            "webhook": "/webhook (GET/POST)",
            "health": "/health"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            return "Forbidden", 403
        return "OK", 200
    
    elif request.method == "POST":
        try:
            data = request.get_json()
            print(f"Received: {data}")
            return jsonify({"status": "received"}), 200
        except Exception as e:
            return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
