from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import warnings
from pandasai import Agent
warnings.filterwarnings("ignore")
from pandasai.helpers import path
import base64
import assemblyai as aai
from dotenv import load_dotenv
import requests
import re

load_dotenv()
app = Flask(__name__)
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Define the folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file has allowed extension
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload_file_and_start_chat', methods=['POST'])
def upload_file_and_start_chat():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Save the file to the uploads folder
        filename = "data.csv"
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('chat'))
    else:
        return 'Invalid file format'

@app.route('/chat')
def chat():
    return render_template('chat.html')

# This route is used to send messages during the chat
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_defined_path = path.find_project_root()
    except ValueError:
        user_defined_path = os.getcwd()
    user_defined_path = os.path.join(user_defined_path, "static", "images")
    user_message = request.form['user_message']
    print(user_message)
    agent = Agent(pd.read_csv("uploads/data.csv"),config={
        "save_charts_path": user_defined_path,
        "save_charts": True,
        "verbose": True,
    })
    response=agent.chat(str(user_message))
    print(response)
    return response

@app.route('/describe',methods=['POST'])
def describe():
    try:
        user_defined_path = path.find_project_root()
    except ValueError:
        user_defined_path = os.getcwd()
    user_message = request.form['user_message']
    user_message = "Do not give chart, just give text, descrive about" + user_message
    agent = Agent(pd.read_csv("uploads/data.csv"),config={
        "save_charts_path": user_defined_path,
        "verbose": True,
    })
    response=agent.chat(str(user_message))
    print(response)
    return response
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_data = request.form['audio_data']
    audio_url = save_audio(audio_data)
    transcript = transcribe(audio_url)
    if transcript.status == aai.TranscriptStatus.error:
        return f"Error: {transcript.error}"
    else:
        return transcript.text
@app.route('/tts', methods=['POST'])
def tts():
    text = request.form['user_message']
    url = "https://api.play.ht/api/v2/tts"

    payload = {
        "text": text,
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

    if response.status_code == 200:
        # Extracting audio URL from the response content
        audio_url_match = re.search(r"url\":\"(.*?)\"", response.text)
        if audio_url_match:
            audio_url = audio_url_match.group(1).replace("\\", "")
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                with open("static/audio.mp3", "wb") as f:
                    f.write(audio_response.content)
                return "Audio file downloaded successfully as audio.mp3"
            else:
                return "Failed to download audio file"
        else:
            return "No audio URL found in the response"
    else:
        return "Failed to get audio URL"

def save_audio(audio_data):
    audio_bytes = base64.b64decode(audio_data.split(",")[1])
    with open("static/audio.mp3", "wb") as f:
        f.write(audio_bytes)
    return "audio.mp3"

def transcribe(audio_url):
    transcriber = aai.Transcriber()
    return transcriber.transcribe("static/audio.mp3")

if __name__ == '__main__':
    # Run the Flask app with production settings
    app.run(host='0.0.0.0', port=5000)
