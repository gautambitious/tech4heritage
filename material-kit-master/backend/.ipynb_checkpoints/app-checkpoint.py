import json
import os
import time
from flask import Flask, render_template, jsonify, request, make_response, send_file, redirect
from flask_cors import CORS
import numpy as np
import efficientnet.tfkeras
import cv2
from tensorflow.keras.models import load_model

app = Flask(__name__)
cors = CORS(app)



@app.route('/', methods=['GET'])
def home():
    return "Monument Photo Enhancer Backend"


@app.route('/getfile', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        path = os.path.join(os.curdir, 'temp', 'input.png')
        f.save(path)
        patch(path)
        print(type(f))
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def patch(path):
    image = cv2.imread('./temp/input.png', cv2.IMREAD_UNCHANGED)
    image.resize(256, 256, 3)
    patched_img = image.reshape(1, 256, 256, 3)
    patch_model = load_model('patch_detection.h5', compile=False)
    p = patch_model.predict(patched_img)
    final = (p.reshape(256, 256) * 256).astype(np.uint8)
    cv2.imwrite('./temp/patched.png', final)


if __name__ == '__main__':
    app.run(debug=True, port=6968)
