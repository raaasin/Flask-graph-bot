from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message']
    return user_message

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
