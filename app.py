from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load("models/model.pkl")

# Define feature names
feature_names = ['Age', 'Gender', 'BMI', 'Smoking', 'GeneticRisk', 'PhysicalActivity', 'AlcoholIntake', 'CancerHistory']

# Define mapping for categorical features
mappings = {
    'Gender': {'Male': 1, 'Female': 0},
    'Smoking': {'Yes': 1, 'No': 0},
    'GeneticRisk': {'Low': 0, 'Medium': 1, 'High': 2},
    'PhysicalActivity': {'Low': 0, 'Medium': 1, 'High': 2},
    'AlcoholIntake': {'Low': 0, 'Medium': 1, 'High': 2},
    'CancerHistory': {'Yes': 1, 'No': 0}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = []
        for feature in feature_names:
            value = request.form[feature]
            if feature in mappings:
                input_data.append(mappings[feature][value])
            else:
                input_data.append(float(value))  # For Age and BMI

        input_df = pd.DataFrame([input_data], columns=feature_names)
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        result = f"{'Positive' if prediction == 1 else 'Negative'} (Probability: {probability:.2f})"
        return render_template('index.html', result=result)
    except Exception as e:
        return render_template('index.html', result="Error in input data!")

if __name__ == '__main__':
    app.run(debug=True)
