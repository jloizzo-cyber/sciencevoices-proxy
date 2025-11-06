from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests

app = Flask(__name__)
from flask_cors import cross_origin

# Allow all domains or specify your domain:
CORS(app, resources={r"/*": {"origins": "*"}})

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/v1/chat/completions", methods=["POST"])
def chat_proxy():
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = request.get_json(force=True)
        r = requests.post(
    "https://api.openai.com/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=60  # prevent hanging
)
# Ensure no streaming mode (stream=True can hang)
payload.pop("stream", None)
        return (r.text, r.status_code, {"Content-Type": "application/json"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "ScienceVoices proxy running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
