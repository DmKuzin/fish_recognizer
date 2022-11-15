#import numpy as np
#import pandas as pd
from flask import Flask, request, render_template
#from sklearn import preprocessing
#import pickle

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))
# cols=['age','workclass','education','marital-status','occupation','relationship','race','gender','capital-gain','capital-loss',
#       'hours-per-week','native-country']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    feature_list = request.form.to_dict()
    imagefile = flask.request.files(str(list(feature_list.values())[0]), '')
#     feature_list = list(feature_list.values())
#     feature_list = list(map(int, feature_list))
#     final_features = np.array(feature_list).reshape(1, 12) 
    
#     prediction = model.predict(final_features)
#     output = int(prediction[0])
#     if output == 1:
#         text = ">50K"
#     else:
#         text = "<=50K"

    #text = "<=50K"
    text = str(list(feature_list.values())[0])
    return render_template('index.html', prediction_text='Employee Income is {}'.format(text))


if __name__ == "__main__":
    app.run(debug=True)
