import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from PIL import Image, ImageOps
#from keras.models import load_model
#import tflite
import tensorflow as tf
#from sklearn import preprocessing
import pickle5

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

model = tf.keras.models.load_model('models/mobileNet.h5')

saved_file_name = 'models/targets_dictionary.pkl'
with open(saved_file_name, 'rb') as f:
    label_name = pickle5.load(f)

print(label_name)

@app.route('/predict',methods=['POST'])
def predict():
    #feature_list = request.form.to_dict()
    #imagefile = request.files.get('img', '')
    file = request.files['img']
    
    pil_image = Image.open(file)
    
    pil_img_sqr = resize_with_padding(pil_image, expected_size=image_size)
    arr_img_sqr = np.asarray(pil_img_sqr) / 256.0

    prediction = label_name[pd.DataFrame(model.predict(arr_img_sqr[None, :])).idxmax(axis=1)[0]]

    # text = "<=50K"
    # print('file:', file)
    # print('pil_image:', pil_image)

    return render_template('index.html', prediction_text='Prediction fish: {}'.format(prediction))


if __name__ == "__main__":
    app.run(debug=True)
