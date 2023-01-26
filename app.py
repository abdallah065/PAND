from __future__ import division, print_function
from gevent.pywsgi import WSGIServer
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import modelClass

# Define a flask app
app = Flask(__name__)

# Load your trained model
model = modelClass.get_model()
# print('Model loaded. Start serving...')


#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print("APP is running now on http://127.0.0.1:5000/")


def model_predict(img_path,model):
    preds = modelClass.predict_image(img_path,model)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/get_classes', methods=['GET','POST'])
def get_classes():
    return modelClass.classes_out


@app.route('/predict', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = modelClass.os.path.dirname(__file__)
        file_path = modelClass.os.path.join(
            basepath, 'uploads', secure_filename(str(f.filename)))
        f.save(file_path)

        # Make prediction
        data = modelClass.predict_image(file_path, model)

        return str(data)

    return "Error"

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5001), app.wsgi_app)
    http_server.serve_forever()
