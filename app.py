from flask import Flask
 
app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def main():
    return "Boston House Price Prediction”
 
 
if __name__ == "__main__":
   app.run()
