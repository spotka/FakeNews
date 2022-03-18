from flask import Flask, render_template, request
import numpy as np
import joblib


app = Flask(__name__)

@app.route('/')


def home():
    return render_template('home.html')

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        # get form data
        text = request.form.get('text')

        try:
            prediction = preprocessDataAndPredict(text)  # pass prediction to template
            return render_template('predict.html', prediction=prediction)

        except ValueError:
            return "Please Enter valid values"

        pass
    pass


def preprocessDataAndPredict(text):
  
    test_data = [text]
    print(test_data)


    # open file
    file = open("Model/text_classification.joblib", "rb")

    # load trained model
    trained_model = joblib.load(file)

    # predict

    prediction = trained_model.predict(test_data)

    return prediction

if __name__ == '__main__':
    app.debug = True
    app.run()