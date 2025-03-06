import os
import requests
import gdown
from flask import Flask, request, jsonify

app = Flask(__name__)

# Model ka filename
MODEL_FILE = "inswapper_128.onnx"

# Google Drive se model download karne ka function
def download_model():
    url = "https://drive.google.com/uc?id=1krOLgjW2tAPaqV-Bw4YALz0xT5zlb5HF"  # Apna Google Drive ID yahan daalo
    gdown.download(url, MODEL_FILE, quiet=False)

# Agar model file missing ho to download karlo
if not os.path.exists(MODEL_FILE):
    print("Model not found! Downloading from Google Drive...")
    download_model()

@app.route('/')
def home():
    return "Face Swap API is running!"

@app.route('/face_swap', methods=['POST'])
def face_swap():
    data = request.json
    source_url = data.get('source')
    target_url = data.get('target')

    if not source_url or not target_url:
        return jsonify({"error": "Source and Target image URLs required"}), 400

    return jsonify({"message": "Face swap process started!", "source": source_url, "target": target_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
