import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"

payload = {
    "text": "\"تَطْوِيرُ نِظامِ ذَكاءٍ اِصْطِناعِيٍّ يُساعِدُ على تَشْخِيصِ الأَمْراضِ: تَمَكَّنَ فَرِيقٌ مِن الباحِثِينَ مِن تَطْوِيرِ نِظامِ ذَكاءٍ اِصْطِناعِيٍّ قادِرٍ عَلَى تَحْلِيلِ الصُوَرِ الطِبِّيَّةِ وَتَشْخِيصِ الأَمْراضِ بِدِقَّةٍ عالِيَةٍ. يُمْكِنُ لِهٰذا النِظامِ أَنْ يُساعِدَ الأَطِبّاءُ فِي تَحْدِيدِ الأَمْراضِ بِشَكْلٍ أَسْرَعَ وَأَكْثَرَ دِقَّةً، مما يُعَزِّزُ جَوْدَةَ الرِعايَةِ الصِحِّيَّة",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "similarity_boost": 0.75,
        "stability": 0.5
    }
}

headers = {
    "xi-api-key": "sk_c4d409c8195d84ef9782d05d5204eccfaf134c577803f964",  # Secure your API key
    "Content-Type": "application/json"
}

# Make the POST request
try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

    # Check and print the response content type
    print("Response Content-Type:", response.headers.get("Content-Type"))

    # If the response is expected to be audio, handle it accordingly
    if response.headers.get("Content-Type") == "audio/mpeg":
        # Save the audio file
        with open("output.mp3", "wb") as audio_file:
            audio_file.write(response.content)
        print("Audio file created: output.mp3")
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