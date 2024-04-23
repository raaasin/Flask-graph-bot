const recordButton = document.getElementById('recordButton');
const transcriptionInput = document.getElementById('userMessage');
const sendButton = document.getElementById('sendButton');

let mediaRecorder;
let chunks = [];
let isRecording = false;

recordButton.addEventListener('click', () => {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
});

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = e => {
                chunks.push(e.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(chunks, { type: 'audio/mp3' });
                const reader = new FileReader();
                reader.onload = () => {
                    sendAudio(reader.result);
                };
                reader.readAsDataURL(audioBlob);
                chunks = [];
            };
            mediaRecorder.start();
            isRecording = true;
            updateButtonUI('🔴 Recording...');
        })
        .catch(err => {
            console.error('Error accessing microphone:', err);
            isRecording = false;
        });
}

function stopRecording() {
    mediaRecorder.stop();
    updateButtonUI('⚪ Processing...');
    recordButton.disabled = true;
}

function sendAudio(audioData) {
    fetch('/transcribe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `audio_data=${encodeURIComponent(audioData)}`
    })
    .then(response => response.text())
    .then(transcription => {
        transcriptionInput.value = transcription;
        isRecording = false;
        recordButton.disabled =false;
        updateButtonUI('🎙️ Start Recording');
    })
    .catch(error => {
        console.error('Error transcribing audio:', error);
        isRecording = false;
        recordButton.disabled =false;
        updateButtonUI('🎙️ Start Recording');
    });
}

function updateButtonUI(text) {
    recordButton.innerText = text;
    sendButton.disabled = false;
    recordButton.disabled =false;
}
