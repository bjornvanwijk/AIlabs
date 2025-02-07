
from flask import Flask, render_template, request, jsonify
from gradio_client import Client
import os
from dotenv import load_dotenv

# Load info from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="static")

# Get Hugging Face credentials
hfApiUrl = os.environ.get('API_url', '')
hfToken = os.environ.get('HF_token', '')

# Initialize Hugging Face client
def get_hf_client():
    return Client(hfApiUrl, hfToken)

# Read system prompt from file
def get_system_prompt():
    try:
        with open('prompt.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "You are a friendly Chatbot."

@app.route("/")
def index():
    return render_template("index.html")

# Define route for text analysis
@app.route("/analyze", methods=["POST"])
def analyze_text():
    try:
        text = request.form['input_text']
        if not text:
            text = " "

        client = get_hf_client()
        system_prompt = get_system_prompt()

        response = client.predict(
            message=text,
            system_message=system_prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )

        analysis = {
            "input": text,
            "analysis": response
        }

        client.close()
        return jsonify({"results": analysis})

    except Exception as err:
        print(f"Error in analyze_text: {str(err)}")
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
