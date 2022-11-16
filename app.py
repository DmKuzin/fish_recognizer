import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from PIL import Image, ImageOps
import tensorflow as tf
import pickle5

app = Flask(__name__)

# input image size
image_size = (256, 256)

# resize image function
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


# load model
model = tf.keras.models.load_model('models/mobileNet.h5')

# load output labels from file
saved_file_name = 'models/targets_dictionary.pkl'
with open(saved_file_name, 'rb') as f:
    label_name = pickle5.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    # read file from request
    file = request.files['img']
    # open file as image
    pil_image = Image.open(file)
    # resize image to network input
    pil_img_sqr = resize_with_padding(pil_image, expected_size=image_size)
    # normalize image and convert to tensor
    arr_img_sqr = np.asarray(pil_img_sqr) / 256.0
    # make prediction
    prediction = label_name[pd.DataFrame(model.predict(arr_img_sqr[None, :])).idxmax(axis=1)[0]]

    return render_template('index.html', prediction_text='Prediction fish: {}'.format(prediction))


if __name__ == "__main__":
    app.run(debug=True)
