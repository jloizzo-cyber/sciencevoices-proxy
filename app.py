import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/")
@app.get("/health")
def health():
    return {"status": "ok", "service": "SciVoices Proxy running"}, 200

@app.post("/v1/chat/completions")
def chat_completions():
    if not OPENAI_API_KEY:
        return jsonify({"error": "OPENAI_API_KEY missing on server"}), 500

    try:
        payload = request.json
        if payload is None:
            return jsonify({"error": "Invalid JSON body"}), 400

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}",
            },
            json=payload,
            timeout=25,
        )
        return jsonify(response.json()), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "OpenAI request timed out"}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
