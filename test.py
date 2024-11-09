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

    async def generate_audio(self, text, title):
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": self.voice_settings
        }

        timeout = aiohttp.ClientTimeout(total=120)  # Set timeout
        retries = 3  # Number of retries

        for attempt in range(retries):
            try:
                # Open an aiohttp session and send a POST request to the API
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.post(self.url, headers=self.headers, json=payload) as response:
                        if response.status != 200:
                            # Raise an exception if the status code is not 200
                            raise Exception(f"Audio generation failed: {await response.text()}")

                        # Read the audio content and save it to a file
                        audio_content = await response.read()
                        audio_file_name = f"{title}.mp3"
                        with open(audio_file_name, "wb") as audio_file:
                            audio_file.write(audio_content)

                        print(f"Audio file created: {audio_file_name}")
                        return  # Exit after successful generation

            except aiohttp.ClientError as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    await asyncio.sleep(2)  # Wait before retrying
                else:
                    raise  # Re-raise the last exception if all attempts fail
# class ElevenLabsWrapper:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
#         self.headers = {
#             "xi-api-key": self.api_key,
#             "Content-Type": "application/json"
#         }
#         self.voice_settings = {
#             "similarity_boost": 0.75,
#             "stability": 0.5
#         }

#     async def generate_audio(self, text, title):
#         payload = {
#             "text": text,
#             "model_id": "eleven_multilingual_v2",
#             "voice_settings": self.voice_settings
#         }

#         timeout = aiohttp.ClientTimeout(total=120)  # Set timeout
#         retries = 3  # Number of retries

#         for attempt in range(retries):
#             try:
#                 async with aiohttp.ClientSession(timeout=timeout) as session:
#                     async with session.post(self.url, headers=self.headers, json=payload) as response:
#                         if response.status != 200:
#                             raise Exception(f"Audio generation failed: {await response.text()}")
#                         audio_content = await response.read()
#                         audio_file_name = f"{title}.mp3"
#                         with open(audio_file_name, "wb") as audio_file:
#                             audio_file.write(audio_content)
#                         print(f"Audio file created: {audio_file_name}")
#                         return  # Exit after successful generation
#             except aiohttp.ClientError as e:
#                 print(f"Attempt {attempt + 1} failed: {e}")
#                 if attempt < retries - 1:
#                     await asyncio.sleep(2)  # Wait before retrying
#                 else:
#                     raise  # Re-raise the last exception if all attempts fail
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
#         self.headers = {
#             "xi-api-key": self.api_key,
#             "Content-Type": "application/json"
#         }
#         self.voice_settings = {
#             "similarity_boost": 0.75,
#             "stability": 0.5
#         }
# async def generate_audio(self, text, title):
#     payload = {
#         "text": text,
#         "model_id": "eleven_multilingual_v2",
#         "voice_settings": self.voice_settings
#     }

#     timeout = aiohttp.ClientTimeout(total=60)  # Set timeout
#     retries = 3  # Number of retries

#     for attempt in range(retries):
#         try:
#             async with aiohttp.ClientSession(timeout=timeout) as session:
#                 async with session.post(self.url, headers=self.headers, json=payload) as response:
#                     if response.status != 200:
#                         raise Exception(f"Audio generation failed: {await response.text()}")
#                     audio_content = await response.read()
#                     audio_file_name = f"{title}.mp3"
#                     with open(audio_file_name, "wb") as audio_file:
#                         audio_file.write(audio_content)
#                     print(f"Audio file created: {audio_file_name}")
#                     return  # Exit after successful generation
#         except aiohttp.ClientError as e:
#             print(f"Attempt {attempt + 1} failed: {e}")
#             if attempt < retries - 1:
#                 await asyncio.sleep(2)  # Wait before retrying
#             else:
#                 raise  # Re-raise the last exception if all attempts fail

#     async def generate_audio(self, text, title):
#         payload = {
#             "text": text,
#             "model_id": "eleven_multilingual_v2",
#             "voice_settings": self.voice_settings
#         }

#         async with aiohttp.ClientSession() as session:
#             async with session.post(self.url, headers=self.headers, json=payload) as response:
#                 if response.status != 200:
#                     raise Exception(f"Audio generation failed: {await response.text()}")
#                 audio_content = await response.read()
#                 audio_file_name = f"{title}.mp3"
#                 with open(audio_file_name, "wb") as audio_file:
#                     audio_file.write(audio_content)
#                 print(f"Audio file created: {audio_file_name}")

# قراءة الحلقات من ملف JSON
def read_prompts_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['episodes']

# استخدام الكود لتوليد النصوص لكل حلقة وتحويلها إلى صوت
async def generate_text_and_audio_for_all_episodes(file_path):
    ibm_wrapper = IBMWatsonXAIWrapper()
    eleven_labs_wrapper = ElevenLabsWrapper(api_key="sk_c4d409c8195d84ef9782d05d5204eccfaf134c577803f964")
    episodes = read_prompts_from_json(file_path)
    
    for episode in episodes:
        title = episode['title']
        prompt = episode['prompt']
        print(f"Generating text for {title}...")

        # توليد النص
        generated_text = await ibm_wrapper.generate_text(prompt)
        print(f"Generated text for {title}:\n{generated_text}\n")

        # تحويل النص إلى صوت
        print(f"Generating audio for {title}...")
        await eleven_labs_wrapper.generate_audio(generated_text, title)

# اختبار الوظائف
file_path = 'episodes.json'  # مسار ملف JSON
asyncio.run(generate_text_and_audio_for_all_episodes(file_path))
