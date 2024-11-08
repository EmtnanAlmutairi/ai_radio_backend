from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv
from database import init_db, save_audio_url, close_db, get_db

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API URLs from environment variables
ALLAM_API_URL = os.getenv('ALLAM_API_URL')
FISH_AUDIO_API_URL = os.getenv('FISH_AUDIO_API_URL')

@app.before_request
def before_request():
    get_db()

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        # Step 1: Call ALLaM API to generate text
        allam_response = requests.post(ALLAM_API_URL, json={'prompt': prompt})
        allam_response.raise_for_status()  # Raise an error for bad responses
        generated_text = allam_response.json().get('text')

        if not generated_text:
            return jsonify({'error': 'No text generated from ALLaM API'}), 500

        # Step 2: Call Fish Audio API to convert text to audio
        fish_audio_response = requests.post(FISH_AUDIO_API_URL, json={'text': generated_text})
        fish_audio_response.raise_for_status()  # Raise an error for bad responses

        # Assuming Fish API returns the audio URL
        audio_url = fish_audio_response.json().get('audio_url')

        # Save the audio URL in the database
        save_audio_url(audio_url)

        return jsonify({'audio_url': audio_url}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        # Initialize the database
        init_db()
    app.run(debug=True)