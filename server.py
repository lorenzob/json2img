'''

curl -H "Content-Type: application/json" -d @rest/request.json localhost:5000/idcard/12345

'''
import os
import time
import glob
import base64
import threading
import sys

import json

from zipfile import ZipFile

from flask import Flask, request, redirect, url_for, Response
from flask import jsonify
from flask import flash
from flask import send_from_directory

from werkzeug.utils import secure_filename

from shutil import copyfile

import datetime
import logging

VERSION="0.1.0"

UPLOAD_FOLDER = 'rest/uploads'
WORK_FOLDER = 'work/'

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['WORK_FOLDER'] = WORK_FOLDER

root_dir = os.path.join(os.path.dirname(os.getcwd()), "json2bins")

@app.route('/')
def index():
    print("index", root_dir)
    return send_from_directory(root_dir, "index.html")

@app.route('/status', methods=['GET'])
def get_status():

    status = [
        {
            'version': VERSION,
            'time': str(datetime.datetime.now())
        }]

    return jsonify({'status': status})


@app.route('/extract', methods=['POST'])
def extract_data():

    print("INIZIO")
    
    try:
      
      response = {
        "items": [
          {
            "filename": "aaa.png",
            "content": "base64 content..."
          }
        ]
      }
      
      print("response", response)
      
      #json_res = json.dumps(response, indent=4)
      
    except Exception as e:
      print(e)
      logging.exception("Generic request error: %s", sys.exc_info()[0])
      #traceback.print_exception(*sys.exc_info())
      response = {
        'version': VERSION,
        'error': "Invalid request: " + str(e)
      }
      #json_res = json.dumps(response, indent=4)
    
    print("fine")
    return jsonify(response)

@app.route('/files/<filename>', methods=['GET',])
def files(filename):
    basename = os.path.basename(filename)
    print(root_dir, basename)
    return send_from_directory(root_dir, basename)

if __name__ == '__main__':

    logging.basicConfig(filename='server.log',level=logging.DEBUG)

    app.run(host='127.0.0.1',port=5005,debug=True,threaded=True)

