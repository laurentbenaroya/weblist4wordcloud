from flask import Flask, request, send_file
from flask import flash, redirect, url_for, render_template
from flask import session, abort
from flask_caching import Cache

from werkzeug.utils import secure_filename

from wordclouds import make_wordcloud

from test_text_file import is_small_to_medium_text_file

import io
import os
import sys
import logging
import string
import random
import matplotlib as plt

import pathlib

from dotenv import load_dotenv
# Load variables from .env file
load_dotenv()


PROG_PATH = pathlib.Path.cwd()
LOG_FILENAME = os.path.join(PROG_PATH, 'main_basic.log')
if True:
    if os.path.isfile(LOG_FILENAME):
        os.remove(LOG_FILENAME)

logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info('BEGIN')
logger.info(PROG_PATH)

UPLOAD_FOLDER = './uploads'
ALLOWED_UPLOAD_EXTENSIONS = {'txt'}
DOWNLOAD_FOLDER = './images'
ALLOWED_DOWNLOAD_EXTENSIONS = {'png', 'jpg'}

app = Flask(__name__)
# Configuration du cache Redis
cache_config = {
    "CACHE_TYPE": "redis",
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
}

# Configuration de Flask-Caching
cache = Cache(app, config=cache_config)

# Configuration de la session Flask pour utiliser Flask-Caching
app.config["SESSION_TYPE"] = "null"
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_CACHE_KEY_PREFIX"] = "session:"
app.config["SESSION_CACHE"] = cache

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

"""
$ pipenv --python 3.9
$ pipenv install
$ python -m textblob.download_corpora
$ pipenv run python main_wordcloud.py
$ 
"""

def allowed_download_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_DOWNLOAD_EXTENSIONS

def allowed_upload_file(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_UPLOAD_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        logger.info(f'post upload file')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/')
        if file and allowed_upload_file(file.filename):
            filename = secure_filename(file.filename)
            local_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_filename)
            max_size = 3500  # limit session cookies is 4093 bytes
            if not is_small_to_medium_text_file(local_filename, max_size=max_size):
                os.remove(local_filename)
                logger.info(f'file detected as no being a text file or file is too large (> {max_size} bytes)')
                return redirect('/')
            session['focus'] = False
            lines = open(local_filename, 'r', encoding='utf-8').readlines()
            for line in lines:
                word = line.strip()
                logger.info(f'found word {word} uploaded index.html')
                session['word_list'].append(word)

            return redirect('/')
        
    return redirect('/')

# word_list = []
# focus = False  # focus on input in html
@app.route('/add', methods=['GET', 'POST'])
def getword():
    if request.method == 'POST':
        logger.info('POST in index.html')
        if 'word' in request.form:
            word = request.form['word']
            if word == '':
                logger.info('enter a word, please')
                session['focus'] = False
                return redirect('/')
            logger.info(f'found word {word} index.html')
            # word_list.append(word)
            session['word_list'].append(word)
            logger.info(word)
            session['focus'] = True
        else:
           session['focus'] = False 
    else:
        session['focus'] = False
    return redirect('/')
    
@app.route("/reset", methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        logger.info('RESET')
        session['word_list'] = []
        session['focus'] = False
    return redirect('/')

@app.route("/submit", methods=['GET', 'POST'])
def generate_file():
    # global response_filename
    if request.method == 'POST':
        session['focus'] = False
        if len(session['word_list']) > 1:
            letter_list = string.ascii_uppercase + string.digits
            filename_length = 15
            response_filename = ''.join(random.choices(letter_list, k=filename_length))+'.jpg'
            logger.info(response_filename)
            if allowed_download_file(response_filename):
                logger.info(response_filename)
                wc = make_wordcloud(session['word_list'], xfig=6, yfig=3)  # aspect ratio
                # Convert the image to bytes
                # img_bytes = io.BytesIO()
                # wc.to_image().save(img_bytes, format='jpeg')
                # img_bytes.seek(0)
                response_filename = os.path.join(app.config['DOWNLOAD_FOLDER'], response_filename)
                wc.to_file(response_filename)
                # Send the file to the client for download
                logger.info('send file')
                return send_file(response_filename, as_attachment=True)
                # return send_file(img_bytes, mimetype='image/jpeg',
                #           as_attachment=True, attachment_filename=response_filename)        
            else:
                logging.info('wrong file extension')      
        else:
            logging.info('needs more words!!!')
    return redirect('/')

@app.route("/")
def index():
    logger.info('I am in index.html')
    if 'start' not in session:
        session['start'] = False
        session['word_list'] = []
        session['focus'] = False
    return render_template("index.html",words= session['word_list'], focus=session['focus'])


if __name__ == "__main__":
    dodebug  = len(sys.argv) > 1 and sys.argv[1] == 'debug'
    app.run(host='0.0.0.0', port=8080, load_dotenv=False, debug=dodebug)
