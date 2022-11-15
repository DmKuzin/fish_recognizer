#import numpy as np
#import pandas as pd
from flask import Flask, request, render_template
#from sklearn import preprocessing
#import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    #feature_list = request.form.to_dict()
    #imagefile = request.files.get('img')
    file = request.files['img']

    text = "<=50K"
    #text = str(list(feature_list.values())[0])
    print('imagefile:', file)
    return render_template('index.html', prediction_text='Employee Income is {}'.format(text))


if __name__ == "__main__":
    app.run(debug=True)
