import numpy as np
#import pandas as pd
from flask import Flask, request, render_template
from PIL import Image, ImageOps
#import tensorflow as tf
#from sklearn import preprocessing
#import pickle

app = Flask(__name__)

image_size = (256, 256)

def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    # print(img.size)
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    #feature_list = request.form.to_dict()
    #imagefile = request.files.get('img', '')
    file = request.files['img']
    
    pil_image = Image.open(file)
    
    pil_img_sqr = resize_with_padding(pil_image, expected_size=image_size)
    arr_img_sqr = np.asarray(pil_img_sqr) / 256.0
    arr_img_sqr[None,:]
    
    text = "<=50K"
    print('file:', file)
    print('pil_image:', pil_image)
  
    return render_template('index.html', prediction_text='Employee Income is {}'.format(text))


if __name__ == "__main__":
    app.run(debug=True)
