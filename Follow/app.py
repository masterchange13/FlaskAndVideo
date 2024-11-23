"""
@Created by Mao on 2024/11/23
@Author:mao
@Github:https://github.com/masterchange13?tab=projects
@Gitee:https://gitee.com/master_change13
 
@File: app.py.py
@IDE: PyCharm
 
@Time: 2024/11/23 16:40
@Motto:不积跬步无以至千里，不积小流无以成江海，程序人生的精彩需要坚持不懈地积累！
@target: 大厂offer，高年薪

@@ written by GuangZhi Mao

@from:
@code target:
"""

# coding: utf-8
from flask import Flask, render_template, Response, request, url_for
import cv2
import numpy as np
import time
import os

app = Flask(__name__)


@app.route('/video', methods=['GET', 'POST'])
def videoshow():
    return render_template('index.html', videourl=url_for('video_feed'))


@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    cap = cv2.VideoCapture('/dev/video0')
    cap.set(3, 600)
    cap.set(4, 480)
    cap.set(5, 40)

    while True:
        ret, img = cap.read()
        ret, jpeg = cv2.imencode('.jpg', img)  # 对图像进行编码输出 jpeg
        yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(host='192.168.2.8', port=5008, debug=True)