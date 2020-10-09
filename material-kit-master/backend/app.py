import json
import os

from flask import Flask, render_template, jsonify, request, make_response, send_file, redirect
from flask_cors import CORS, cross_origin
from PIL import Image
import numpy as np
import efficientnet.tfkeras
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
        path = os.path.join(os.curdir, 'temp', f.filename)
        f.save(path)
        # patched, final = process(path)
        print(type(f))
    return redirect('/index.html', code=302)
    # return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


def process(path):
    image = np.array(Image.open('check.png'))
    model = load_model('patch_detection.h5', compile=False)
    patched_img = np.array(Image.open('check.png'))


if __name__ == '__main__':
    app.run(debug=True, port=6968)
