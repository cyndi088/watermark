# -*- coding: utf-8 -*-
import cv2
import urllib
import numpy as np
from flask import Flask
from flask import jsonify
from flask import request
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)

executor = ThreadPoolExecutor(10)    # 同时处理的最大线程数


@app.route('/', methods=['GET'])
def index():
    return "Hello，欢迎访问API！"


@app.route('/imgurl', methods=['POST'])
def get_rtsp():
    img = Img()
    url = request.form.get('url')
    img_url = img.func(url)
    if img_url:
        img_url = img_url
        status = 1
    else:
        img_url = url
        status = 2
    output = {'img_url': img_url, 'status': status}
    return jsonify(output)


class Img(object):

    def func(self, url):
        # 读入图像,三通道
        # image = cv2.imread("test/1.png", cv2.IMREAD_COLOR)  # timg.jpeg
        img_name = url.split('/')[-1]
        img_format = img_name.split('.')[-1]
        resp = urllib.request.urlopen(url)
        # bytearray将数据转换成（返回）一个新的字节数组
        # asarray 复制数据，将结构化数据转换成ndarray
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        # cv2.imdecode()函数将数据解码成Opencv图像格式
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # 读入图像尺寸
        cols, rows, _ = image.shape
        # 缩放比例
        ratio = 0.8

        # 缩放后的尺寸
        cols = int(ratio * cols)
        rows = int(ratio * rows)

        # 缩放图片
        image = cv2.resize(image, (rows, cols))

        # 获得三个通道
        Bch, Gch, Rch = cv2.split(image)

        # 红色通道的histgram
        # 变换程一维向量
        pixelSequence = Rch.reshape([rows*cols, ])

        # 统计直方图的组数
        numberBins = 256

        # histogram, bins, patch = plt.hist(pixelSequence, numberBins, facecolor='black', histtype='bar')  # facecolor设置为黑色

        # 红色通道阈值
        _, RedThresh = cv2.threshold(Rch, 130, 255, cv2.THRESH_BINARY)

        # 膨胀操作
        # element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # erode = cv2.erode(RedThresh, element)

        # 显示效果
        # cv2.imwrite(img_name, RedThresh)
        cv2.imencode('.%s' % img_format, RedThresh)[1].tofile('../tmp/%s' % img_name)
        path = 'http://192.168.10.125:3000'
        img_path = path + '/tmp/%s' % img_name
        return img_path


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
    # url = "http://114.55.75.34:85/sp201811/M00/00/91/Chibolv0_cyAVk19AAF7Scw0SQ8702.png"

