#import numpy as np
#import pandas as pd
from flask import Flask, request, render_template
from PIL import Image
#import tensorflow as tf
#from sklearn import preprocessing
#import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    #feature_list = request.form.to_dict()
    imagefile = request.files.get('img', '')
    file = request.files['img']
    
    pil_image = Image.open(file)
    
    #bits = tf.io.read_file(file)

    text = "<=50K"
    #text = str(list(feature_list.values())[0])
    print('imagefile:', imagefile)
    print('file:', file)
    print('pil_image:', pil_image)
    #print('bits:', bits)
  
    return render_template('index.html', prediction_text='Employee Income is {}'.format(text))


if __name__ == "__main__":
    app.run(debug=True)
