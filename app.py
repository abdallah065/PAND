from __future__ import division, print_function


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import modelClass

# Define a flask app
app = Flask(__name__)

# Load your trained model
model = modelClass.get_model()
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
print('Model loaded. Check http://127.0.0.1:5000/')


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
        preds = model_predict(file_path, model)

        # # Process your result for human
        # pred_class = preds.argmax(axis=-1)    # Simple argmax
                   
        # # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        # # result = str(pred_class[0][0][1])               # Convert to string
        
        # # pred_class = int(pred_class)
        # classes ={0: "ALL", 1: "AML", 2: "CLL", 3: "CML"}

        # return str("The image is classified as: "+str(classes[pred_class]))
        return str(preds)

    return "Error"


if __name__ == '__main__':
    app.run(debug=True)

