from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

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
        filename = file.filename
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
    user_message = request.form['user_message']
    # Here, you would implement your logic to process the user message and generate a response
    # For demonstration purposes, let's just return the user message itself
    return user_message

if __name__ == '__main__':
    app.run(debug=True)
