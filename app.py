from flask import Flask
 
app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def main():
    return print('test')
 
 
if __name__ == "__main__":
   app.run(debug=True)
