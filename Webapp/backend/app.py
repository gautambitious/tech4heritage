# import sys

# sys.modules[__name__].__dict__.clear()
import json
import os
from flask import Flask, request
from flask_cors import CORS
import shutil
from restoration import Restoration

app = Flask(__name__)
cors = CORS(app)


models = Restoration()


@app.route('/', methods=['GET'])
def home():
    return "This is the Backend of the Application. Please open Index.html to get started"


@app.route('/getfile', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        path = os.path.join(os.curdir, 'temp', 'input.png')
        f.save(path)
        models.give_result()
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/feedback/yes', methods=['POST', 'GET'])
def yes():
    if request.method == 'POST':
        with open('./data/liked/index.txt', 'r') as f:
            index = int(f.read())
        shutil.copy('./temp/input.png', './data/liked/inputs/{}.png'.format(index))
        shutil.copy('./temp/temp_mask.jpg', './data/liked/masks/{}.jpg'.format(index))
        shutil.copy('./temp/restored.png', './data/liked/outputs/{}.png'.format(index))
        shutil.copy('./temp/patched.png', './data/liked/patches/{}.png'.format(index))
        with open('./data/liked/index.txt', 'w') as f:
            f.write(str(index+1))

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/feedback/no', methods=['POST', 'GET'])
def no():
    if request.method == 'POST':
        with open('./data/disliked/index.txt', 'r') as f:
            index = int(f.read())
        shutil.copy('./temp/input.png', './data/disliked/inputs/{}.png'.format(index))
        shutil.copy('./temp/temp_mask.jpg', './data/disliked/masks/{}.jpg'.format(index))
        shutil.copy('./temp/restored.png', './data/disliked/outputs/{}.png'.format(index))
        shutil.copy('./temp/patched.png', './data/disliked/patches/{}.png'.format(index))
        with open('./data/disliked/index.txt', 'w') as f:
            f.write(str(index+1))

        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True, port=6968)
