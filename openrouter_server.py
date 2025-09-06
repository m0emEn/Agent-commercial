# server_openrouter.py
from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # <-- allow cross-origin requests

# Set your OpenRouter API key as an environment variable
OPENROUTER_API_KEY = "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"

@app.route("/generate_pitch", methods=["POST"])
def generate_pitch():
    """
    Expects JSON:
    {
        "client_id": 47836,
        "age": 35,
        "recommended_products": ["Product A", "Product B"]
    }
    Returns a JSON with the pitch.
    """
    data = request.json

    client_id = data.get("client_id")
    age = data.get("age")
    job=data.get("job")
    type=data.get("type")
    recommended_products = data.get("recommended_products")

    if not client_id or not recommended_products:
        return jsonify({"error": "Missing client_id or recommended_products"}), 400

    # Prepare the prompt
    if type!='MORALE':
        prompt = (
        f"Generate a persuasive and professional marketing pitch for a client aged {age}.working as {job} "
        f"Include only these products: {', '.join(recommended_products)}. "
        "Do NOT include greetings, explanations, or any extra text. "
        "Return only the pitch text."
        "in french and speak as an employee of bh assurance"
    )
    else:
        prompt = (
        f"Generate a persuasive and professional marketing pitch for an entreprise.working as {job} "
        f"Include only these products: {', '.join(recommended_products)}. "
        "Do NOT include greetings, explanations, or any extra text. "
        "Return only the pitch text."
        "in french and speak as an employee of bh assurance"
    )


    # OpenRouter API request
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat-v3.1:free",  # You can choose another model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        pitch = result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

    return jsonify({
        "client_id": client_id,
        "pitch": pitch
    })

if __name__ == "__main__":
    app.run(debug=True)
