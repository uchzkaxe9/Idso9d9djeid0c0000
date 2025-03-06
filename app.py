import cv2
import numpy as np
import requests
import base64
from flask import Flask, request, send_file
import insightface
from insightface.app import FaceAnalysis
import tempfile
import os

app = Flask(__name__)

# InsightFace Model Load
face_swapper = insightface.model_zoo.get_model('inswapper_128.onnx')
face_analysis = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_analysis.prepare(ctx_id=0, det_size=(640, 640))

# Function: Convert Image URL to NumPy Array
def url_to_image(url):
    response = requests.get(url)
    image_array = np.frombuffer(response.content, dtype=np.uint8)
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

@app.route('/api/faceswap', methods=['GET'])
def face_swap():
    # GET Parameters
    face_swap_url = request.args.get('face_swap')
    target_url = request.args.get('target')

    if not face_swap_url or not target_url:
        return {'error': 'face_swap aur target parameters required'}, 400

    # Load Images
    source_img = url_to_image(face_swap_url)
    target_img = url_to_image(target_url)

    # Detect Faces
    src_faces = face_analysis.get(source_img)
    tgt_faces = face_analysis.get(target_img)

    if len(src_faces) == 0 or len(tgt_faces) == 0:
        return {'error': 'Face detection failed'}, 400

    # Perform Face Swap
    swapped_img = face_swapper.get(target_img, tgt_faces[0], source_img, src_faces[0], paste_back=True)

    # Save Image Temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    cv2.imwrite(temp_file.name, swapped_img)

    # Serve Image
    return send_file(temp_file.name, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
