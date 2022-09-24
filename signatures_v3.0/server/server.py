directory = './files/'
import os
import base64
import re

try:
    import http.server as server
except ImportError:
    import SimpleHTTPServer as server

# MODEL
import cv2
import numpy as np
from random import shuffle
from tqdm import tqdm
import matplotlib.pyplot as plt
import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

TRAIN_DIR = 'C:/Users/User/Desktop/Desktop/SIGNATURE_v2.0/data/train'
TEST_DIR = './files'
IMG_SIZE = 100
LR = 9e-6

MODEL_NAME = 'signatures-{}-{}.model'.format(LR, '2conv')

# -------------------------
tf.reset_default_graph()
convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input')

convnet = conv_2d(convnet, 32, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 3, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 32, 3, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 2, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet)
# ------------------------
if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print('model loaded')
# ========================
class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
    def do_POST(self):
        i = 1
        filename = directory + f'{i}.png'
        while True:
            if (os.path.exists(filename) == False):
                break
            else:
                i = i + 1
                filename = directory + f'{i}.png'
        file_length = int(self.headers['Content-Length'])
        image_b64 = self.rfile.read(file_length)
        imgdata = re.sub('^data:image/.+;base64,', '', image_b64.decode())
        imgdata = base64.b64decode(imgdata)
        with open(filename, 'wb') as f:
            f.write(imgdata)

        path = filename
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
        img = img.reshape(IMG_SIZE, IMG_SIZE, 1)
        model_out = model.predict([img])[0]
        print('Result:')
        print(model_out)
        if np.argmax(model_out) == 1: str_label = 'Sergeev'
        else: str_label = 'Ivanov'
            
        # ====

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        reply_body = '{"status" : "' + str_label + '"}\n'
        self.wfile.write(reply_body.encode('utf-8'))
        return

if __name__ == '__main__':
    server.test(HandlerClass=HTTPRequestHandler)
