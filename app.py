#-*- coding:utf-8 -*-
from flask import Flask, request, jsonify, render_template
from routes import init_route
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

@app.route('/upload', methods=['POST'])
def upload():
    images = []
    basedir = os.path.abspath(os.path.dirname(__file__))
    updir = os.path.join(basedir, 'static/upload/')
    files = request.files

    index = 0
    results = []
    for f in files:
        file = files[f]
        filename = secure_filename(file.filename)
        filePath = os.path.join(updir, filename)
        file.save(filePath)
        print "file path:"
        print filePath

        try:
            image_data = read_image2RGBbytesFrom(filePath)
        except:
            print "读取图片失败"

        filePath = 'static/upload/'+filename
        try:
            predictions = sess.run(softmax_tensor, \
                         {'DecodeJpeg/contents:0': image_data})
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            re = {}
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                re[human_string] = '%.5f' % score
            re['url'] = filePath
            results.append(re)
        except:
            print "预测失败"
    return render_template('result.html', results=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=argv[1])


