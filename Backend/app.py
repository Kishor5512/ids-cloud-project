from flask import Flask, request, jsonify
import os
import joblib
import numpy as np

app = Flask(__name__)

# Load model safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(model_path)

@app.route('/')
def home():
    return "IDS API Running ✅"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Validate input
        if not data or 'features' not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400

        features = data['features']

        if len(features) != 78:
            return jsonify({"error": "Expected 78 features"}), 400

        # Convert to numpy array
        features = np.array(features).reshape(1, -1)

        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0].max()

        return jsonify({
            "prediction": int(prediction),
            "confidence": float(prob)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)