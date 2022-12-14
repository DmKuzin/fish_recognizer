import numpy as np
import pandas as pd
from flask import Flask, request, flash, redirect, render_template
from PIL import Image, ImageOps
import tensorflow as tf
import pickle
import werkzeug

app = Flask(__name__)

# input image size
image_size = (256, 256)
# allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp'}


# check file on allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# resize image function
# def resize_with_padding(img, expected_size):
#     img.thumbnail((expected_size[0], expected_size[1]))
#     # print(img.size)
#     delta_width = expected_size[0] - img.size[0]
#     delta_height = expected_size[1] - img.size[1]
#     pad_width = delta_width // 2
#     pad_height = delta_height // 2
#     padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
#     return ImageOps.expand(img, padding)

# Open file and convert to input network format
def decode_image_from_file(filename, image_size=image_size):
    pil_img = Image.open(filename)
    pil_img_rgb = pil_img.convert('RGB')
    pil_img_rgb_arr = np.asarray(pil_img_rgb)
    image = tf.cast(pil_img_rgb_arr, tf.float32) / 255.0
    image = tf.image.resize_with_pad(image,
                                     target_height=image_size[0],
                                     target_width=image_size[1],
                                     method=tf.image.ResizeMethod.BILINEAR,
                                     antialias=False
                                     )

    return image


@app.route('/')
def home():
    return render_template('index.html')


# load model
model = tf.keras.models.load_model('models/DensNet121.h5')

# load output labels from file
df_label_name_load = pd.read_csv('models/label_name.csv', index_col=0)


# saved_file_name = 'models/targets_dictionary.pkl'
# with open(saved_file_name, 'rb') as f:
#     label_name = pickle.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    # read file from request
    file = request.files['img']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return render_template('index.html', prediction_text='No selected file')
    if file and allowed_file(file.filename):
        # filename = werkzeug.utils.secure_filename(file.filename)
        # print('file: ', file)
        # print('filename:', filename)
        arr_img_sqr = decode_image_from_file(file)
        pred_idx = pd.DataFrame(model.predict(arr_img_sqr[None, :])).idxmax(axis=1)[0]
        prediction = df_label_name_load.iloc[[pred_idx]]['rus'].values[0]

        return render_template('index.html', prediction_text='Prediction fish: {}'.format(prediction))


if __name__ == "__main__":
    app.run(debug=True)
