from flask import Flask, jsonify, request
import requests
import os
from flask_cors import CORS
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API URL from environment variables
FISH_AUDIO_API_URL = os.getenv('FISH_AUDIO_API_URL')

@app.route('/convert-episodes-to-audio', methods=['POST'])
def convert_episodes_to_audio():
    """Convert episodes from JSON to audio using Fish Audio API."""
    try:
        # قراءة بيانات الحلقات من ملف JSON
        with open('episodes.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        audio_urls = []  # قائمة لحفظ روابط الصوت الناتجة

        # إرسال كل حلقة إلى Fish Audio API
        for episode in data['episodes']:
            episode_content = episode['content']
            response = requests.post(
                FISH_AUDIO_API_URL,
                json={'text': episode_content},
                headers={'Authorization': f'Bearer {os.getenv("FISH_AUDIO_API_KEY")}'}
            )
            response.raise_for_status()  # تحقق من نجاح الطلب
            audio_url = response.json().get('audio_url')
            audio_urls.append({'title': episode['title'], 'audio_url': audio_url})

        return jsonify(audio_urls), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except FileNotFoundError:
        return jsonify({'error': 'episodes.json file not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Error parsing JSON'}), 500

if __name__ == '__main__':
    app.run(debug=True)