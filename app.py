#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
from routes import init_route, processUpload, classifycategory, classifymogutou
# import cv2

import numpy as np
from PIL import Image, ImageSequence
import os
import sys
import requests
from StringIO import StringIO
import datetime
from sys import argv

reload(sys)
print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


app = Flask(__name__)
init_route(app)

@app.route('/classify/upload', methods=['POST'])
def upload():
    files = request.files
    return processUpload(files)


@app.route('/classify', methods=['POST'])
def classify():
    url = request.url
    return classifycategory(request.form['url'])


@app.route('/classify/mogutou', methods=['POST'])
def mogutou():
    url = request.url
    return classifymogutou(request.form['url'])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=argv[1])


