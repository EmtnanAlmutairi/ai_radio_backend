import aiohttp
import asyncio
import json
class IBMWatsonXAIWrapper:
    def __init__(self):
        self.api_key = "0AjxrvhaH_-8on2m2E_VbDs7NMGuiPz_WQ8bTmgqMZEF"
        self.project_id = "3464a2f9-88a4-4992-8e0c-adf8c3967ffd"
        self.url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
        self.model_id = "sdaia/allam-1-13b-instruct"
        self.parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 400,
            "temperature": 0.7,
            "top_p": 1,
            "repetition_penalty": 1.0
        }
        self.access_token = None
        self.headers = None
    async def get_access_token(self):
        token_url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, headers=headers, data=data) as response:
                response_json = await response.json()
                return response_json["access_token"]
    async def generate_text(self, prompt):
        if not self.access_token:
            self.access_token = await self.get_access_token()
            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
        body = {
            "input": f"<s> [INST] {prompt} [/INST]",
            "parameters": self.parameters,
            "model_id": self.model_id,
            "project_id": self.project_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, json=body) as response:
                if response.status != 200:
                    raise Exception(f"Non-200 response: {await response.text()}")
                data = await response.json()
                return data.get('results', [{}])[0].get('generated_text', "No text generated")
    async def send_to_api(self, title, content, file_url):
        api_url = "https://radioallam.devadnan.net/insert.php"
        payload = {
            "title": title,
            "content": content,
            "audio_url": file_url
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=payload) as response:
                if response.status == 200:
                    response_data = await response.json()
                    print(f"Successfully Insert data to db: {response_data}")
                else:
                    print(f"Failed to send data to API: {await response.text()}")
class ElevenLabsWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        self.voice_settings = {
            "similarity_boost": 0.75,
            "stability": 0.5
        }
    async def upload_audio(self, audio_file_name):
        upload_url = "https://radioallam.devadnan.net/index.php"
        async with aiohttp.ClientSession() as session:
            with open(audio_file_name, 'rb') as file:
                data = aiohttp.FormData()
                data.add_field('file', file, filename=audio_file_name, content_type='audio/mpeg')
                try:
                    async with session.post(upload_url, data=data) as response:
                        content_type = response.headers.get('Content-Type', '').lower()
                        if 'application/json' in content_type:
                            response_json = await response.json()
                            file_url = response_json.get("file_url", "")
                            if file_url:
                                return file_url
                            else:
                                raise Exception(f"Error: File URL not found in response.")
                        else:
                            response_text = await response.text()
                            raise Exception(f"Unexpected response type: {content_type}. Response text: {response_text}")
                except aiohttp.ClientError as e:
                    print(f"Upload failed: {e}")
                    raise
    async def generate_audio(self, text, title):
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": self.voice_settings
        }
        timeout = aiohttp.ClientTimeout(total=120)
        retries = 3
        for attempt in range(retries):
            try:
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(self.url, headers=self.headers, json=payload) as response:
                        if response.status != 200:
                            raise Exception(f"Audio generation failed: {await response.text()}")

                        audio_content = await response.read()
                        audio_file_name = f"{title}.mp3"
                        with open(audio_file_name, "wb") as audio_file:
                            audio_file.write(audio_content)
                        file_url = await self.upload_audio(audio_file_name)
                        ibm_wrapper = IBMWatsonXAIWrapper() 
                        await ibm_wrapper.send_to_api(title, text, file_url)  
                        return file_url  
            except aiohttp.ClientError as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(2)
                else:
                    raise
def read_prompts_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['episodes']
async def generate_text_and_audio_for_all_episodes(file_path):
    ibm_wrapper = IBMWatsonXAIWrapper()
    eleven_labs_wrapper = ElevenLabsWrapper(api_key="sk_c4d409c8195d84ef9782d05d5204eccfaf134c577803f964")
    episodes = read_prompts_from_json(file_path)
    for episode in episodes:
        title = episode['title']
        prompt = episode['prompt']
        print(f"Generating text for {title}...")
        generated_text = await ibm_wrapper.generate_text(prompt)
        print(f"Generated text for {title}:\n{generated_text}\n")
        print(f"Generating audio for {title}...")
        file_url = await eleven_labs_wrapper.generate_audio(generated_text, title)
        print(f"Audio available at: {file_url}")
file_path = 'episodes.json'
asyncio.run(generate_text_and_audio_for_all_episodes(file_path))
