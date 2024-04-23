from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import warnings
from pandasai import Agent
warnings.filterwarnings("ignore")
from pandasai.helpers import path
import base64
import assemblyai as aai

app = Flask(__name__)
aai.settings.api_key = "4822f34dd0bb40e9a1be096507478a73"

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

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_data = request.form['audio_data']
    audio_url = save_audio(audio_data)
    transcript = transcribe(audio_url)
    if transcript.status == aai.TranscriptStatus.error:
        return f"Error: {transcript.error}"
    else:
        return transcript.text

def save_audio(audio_data):
    audio_bytes = base64.b64decode(audio_data.split(",")[1])
    with open("audio.mp3", "wb") as f:
        f.write(audio_bytes)
    return "audio.mp3"

def transcribe(audio_url):
    transcriber = aai.Transcriber()
    return transcriber.transcribe(audio_url)

if __name__ == '__main__':
    # Run the Flask app with production settings
    app.run(host='0.0.0.0', port=3000)
