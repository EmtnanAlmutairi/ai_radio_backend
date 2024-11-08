import requests
import json

# Load JSON data from the file
with open('episodes.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Loop through each episode and create audio files
for episode in data["episodes"]:
    title = episode["title"]
    content = episode["content"]

    print(f"Processing: {title}")

    # Prepare the payload for the API request
    payload = {
        "text": content,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "similarity_boost": 0.75,
            "stability": 0.5
        }
    }

    headers = {
        "xi-api-key": "sk_c4d409c8195d84ef9782d05d5204eccfaf134c577803f964",  # Keep this secure
        "Content-Type": "application/json"
    }

    # Make the POST request
    try:
        response = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB", json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Check and print the response content type
        print("Response Content-Type:", response.headers.get("Content-Type"))

        # If the response is expected to be audio, handle it accordingly
        if response.headers.get("Content-Type") == "audio/mpeg":
            # Save the audio file with the episode title
            audio_file_name = f"{title}.mp3"
            with open(audio_file_name, "wb") as audio_file:
                audio_file.write(response.content)
            print(f"Audio file created: {audio_file_name}")
        else:
            # Print the response text for debugging
            print("Response text:", response.text)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
        print("Response content:", response.text)  # Show raw response content
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # General request error
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Any other exceptions