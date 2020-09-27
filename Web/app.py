import os
from os import listdir

from flask import Flask, request, render_template, redirect, flash
from flask_dropzone import Dropzone

app = Flask(__name__)
app.secret_key = 'abc'
app.config['UPLOAD_FOLDER'] = os.getcwd() + r'\uploads'
app.config['DROPZONE_MAX_FILES'] = 1
app.config['DROPZONE_DEFAULT_MESSAGE'] = 'Drop Files Here To Enhance Your Monument\'s Image'
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
app.config['DROPZONE_REDIRECT_URL'] = 'results'

dropzone = Dropzone(app)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/uploads', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        f = request.files.get('file')
        print(type(request.files))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))

        return redirect('/results')

    return 'upload template'


@app.route('/results', methods=['GET'])
def results():
    print(len(listdir(os.getcwd() + r'\uploads')))
    if len(listdir(os.getcwd() + r'\uploads')) == 0:
        return flash('No Files Uploaded', 'error')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
