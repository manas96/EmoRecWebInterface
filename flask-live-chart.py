import json
from time import time
from random import random
from flask import Flask, render_template, make_response
import os
import pickle

inputCamera = 0
farmeSkip = 10


app = Flask(__name__)
#realtime_plot.run(inputCamera, farmeSkip)
#os.system('python faceRecog/realtime_plot.py 0 10 &')

@app.route('/')
def hello_world():
    return render_template('index.html', data='test')

@app.route('/live-data')
def live_data():
    
  #  data = [time() * 1000, random() * 100]
    readFile = 'faceRecog/testfile'
    #readFile = 'emorec/flaskPipe'
    with open(readFile, 'rb') as fp:
        receivedData = pickle.load(fp)
        #receivedData format:
        #[a, d, h, n, sad, sur, frame]
        print('Received data is : ',receivedData)
    
    response = make_response(json.dumps(receivedData))
    response.content_type = 'application/json'
    return response




app.run(debug=True, host='127.0.0.1', port=5000)
