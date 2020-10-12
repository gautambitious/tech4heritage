import json
import os
from flask import Flask,  request
from flask_cors import CORS
from restoration import Restoration

app = Flask(__name__)
cors = CORS(app)
models = Restoration()


@app.route('/', methods=['GET'])
def home():
    return "Monument Photo Enhancer Backend"


@app.route('/getfile', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        path = os.path.join(os.curdir, 'temp', 'input.png')
        f.save(path)
        models.give_result()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


# def patch(path):
#     image = cv2.imread('./temp/input.png', cv2.IMREAD_UNCHANGED)
#     image.resize(256, 256, 3)
#     patched_img = image.reshape(1, 256, 256, 3)
#     patch_model = load_model('patch_detection.h5', compile=False)
#     p = patch_model.predict(patched_img)
#     final = (p.reshape(256, 256) * 256).astype(np.uint8)
#     cv2.imwrite('./temp/patched.png', final)


if __name__ == '__main__':
    app.run(debug=True, port=6968)
