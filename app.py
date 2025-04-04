from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np

# Load pre-trained models and preprocessor
lr_model = joblib.load("model/lr_model.joblib")
svm_model = joblib.load("model/svm_model.joblib")
preprocessor = joblib.load("model/preprocessor.joblib")

# Define the categorical and numerical features
categorical_features = ['job', 'marital', 'education', 'default', 'housing', 'loan',
                        'contact', 'month', 'day_of_week', 'poutcome']
numerical_features = ['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate',
                      'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have an 'index.html' template

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Receive input data as JSON

        # Prepare the input for prediction
        manual_input = pd.DataFrame([{
            'age': data['age'], 'duration': np.nan, 'campaign': np.nan, 'pdays': np.nan, 'previous': np.nan,
            'emp.var.rate': np.nan, 'cons.price.idx': np.nan, 'cons.conf.idx': np.nan,
            'euribor3m': np.nan, 'nr.employed': np.nan,
            'job': data['job'], 'marital': data['marital'], 'education': data['education'], 'default': data['default'],
            'housing': data['housing'], 'loan': data['loan'], 'contact': np.nan, 'month': np.nan,
            'day_of_week': np.nan, 'poutcome': np.nan
        }])

        # Fill missing numerical data with 0 and categorical data with 'unknown'
        manual_input[numerical_features] = manual_input[numerical_features].fillna(0)
        manual_input[categorical_features] = manual_input[categorical_features].fillna('unknown')
        
        # Preprocess the input
        manual_transformed = preprocessor.transform(manual_input)

        # Make prediction using the logistic regression model
        prediction = lr_model.predict(manual_transformed)
        
        # Return the prediction as JSON
        return jsonify({"Subscribed": prediction[0]})
    
    except Exception as e:
        # Return error message in case of failure
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
