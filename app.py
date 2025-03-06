import os
import requests
import gdown
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

MODEL_FILE = "inswapper_128.onnx"

def download_model():
    url = "https://drive.google.com/uc?id=1krOLgjW2tAPaqV-Bw4YALz0xT5zlb5HF"
    gdown.download(url, MODEL_FILE, quiet=False)

if not os.path.exists(MODEL_FILE):
    print("Model not found! Downloading from Google Drive...")
    download_model()

@app.route('/')
def home():
    return "Face Swap API is running!"

@app.route('/face_swap', methods=['GET', 'POST'])
def face_swap():
    if request.method == 'POST':
        data = request.json
        source_url = data.get('source')
        target_url = data.get('target')
    else:
        source_url = request.args.get('source')
        target_url = request.args.get('target')

    if not source_url or not target_url:
        return jsonify({"error": "Source and Target image URLs required"}), 400

    # Dono images ko download karna
    source_path = "source.jpg"
    target_path = "target.jpg"
    
    with open(source_path, "wb") as f:
        f.write(requests.get(source_url).content)

    with open(target_path, "wb") as f:
        f.write(requests.get(target_url).content)

    # Dummy face swap (Tum yahan actual model ka code daal sakte ho)
    swapped_path = "swapped.jpg"
    os.system(f"cp {source_path} {swapped_path}")  # Yeh sirf testing ke liye hai, face swap model ka code lagana padega

    return send_file(swapped_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
