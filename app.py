from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

# Load pre-trained models and preprocessor
lr_model = joblib.load("model/lr_model.joblib")
svm_model = joblib.load("model/svm_model.joblib")
preprocessor = joblib.load("model/preprocessor.joblib")

# Define the categorical and numerical features
categorical_features = ['job', 'marital', 'education', 'default', 'housing', 'loan',
                        'contact', 'month', 'day_of_week', 'poutcome']
numerical_features = ['age', 'balance','duration', 'campaign', 'pdays', 'previous', 'emp.var.rate',
                      'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']

app = Flask(__name__)

def prepare_input(data):
    return pd.DataFrame([{
        "age": int(data["age"]),
        "balance": float(data["balance"]),
        "job": data["job"],
        "marital": data["marital"],
        "education": data["education"],
        "default": data["default"],
        "housing": data["housing"],
        "loan": data["loan"],
        "contact": data.get("contact", "cellular"),
        "month": data.get("month", "may"),
        "day_of_week": data.get("day_of_week", "mon"),
        "campaign": 1,
        "pdays": 0,
        "previous": 0,
        "duration": int(data.get("duration", 200)),
        "poutcome": "nonexistent",
        "emp.var.rate": 1.1,
        "cons.price.idx": 93.994,
        "cons.conf.idx": -36.1,
        "euribor3m": 4.857,
        "nr.employed": 5191.0
    }])



@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have an 'index.html' template

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Missing JSON input"}), 400

        input_df = prepare_input(data)
        
        input_df[numerical_features] = input_df[numerical_features].fillna(0)
        input_df[categorical_features] = input_df[categorical_features].fillna('unknown')
        
        manual_transformed = preprocessor.transform(input_df)
        prediction = lr_model.predict(manual_transformed)
        
        return jsonify({"Subscribed": prediction[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Return error message in case of failure
        return jsonify({"error": str(e)})

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=80)

