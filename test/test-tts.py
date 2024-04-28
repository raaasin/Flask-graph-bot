import requests

url = "https://api.play.ht/api/v2/tts"

payload = {
    "text": "The data required to plot isn't enough, could you please specify with more key points that i could use to plot such a graph?",
    "voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
    "output_format": "mp3",
    "voice_engine": "PlayHT2.0",
    "quality": "medium",
    "speed": 0.89,
    "sample_rate": 24000,
    "seed": None,
    "temperature": None,
    "emotion": "female_happy",
    "voice_guidance": 3,
    "style_guidance": 20
}
headers = {
    "accept": "text/event-stream",
    "content-type": "application/json",
    "AUTHORIZATION": "16ccb21b1c334a868742706ac41ffec7",
    "X-USER-ID": "0XcJ8TomjCW0Z6tKARcA8ZTM0Vo1"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)