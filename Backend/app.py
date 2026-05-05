from flask import Flask, request, jsonify,render_template_string
import os
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

model = joblib.load(model_path)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>IDS Real-Time Dashboard</title>

    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .container {
            background: #111827;
            padding: 25px;
            border-radius: 15px;
            width: 750px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
        }

        h2 {
            margin-bottom: 5px;
        }

        p {
            color: #9ca3af;
        }

        .stats {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
        }

        .card {
            background: #1f2937;
            padding: 15px;
            border-radius: 10px;
            width: 30%;
            font-size: 18px;
        }

        .card.attack {
            border-left: 5px solid red;
        }

        .card.safe {
            border-left: 5px solid green;
        }

        textarea {
            width: 100%;
            height: 150px;
            border-radius: 10px;
            border: none;
            padding: 10px;
            background: #1f2937;
            color: white;
            margin-top: 10px;
        }

        button {
            margin-top: 15px;
            background: #22c55e;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #16a34a;
        }

        #result {
            margin-top: 15px;
            font-size: 18px;
        }

        #logs {
            background: #000;
            padding: 10px;
            height: 150px;
            overflow-y: auto;
            text-align: left;
            font-size: 12px;
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
</head>

<body>

<div class="container">

    <h2> IDS Real-Time Dashboard</h2>
    <p>Analyze and monitor network traffic</p>

    <div class="stats">
        <div class="card">Total: <span id="total">0</span></div>
        <div class="card attack">Attacks: <span id="attacks">0</span></div>
        <div class="card safe">Normal: <span id="normal">0</span></div>
    </div>

    <textarea id="inputData">
{
  "features": [12,8456721,7,10,95,150,22,1,8.45,9.12,28,1,10.21,11.32,20.45,1.85,320145.12,845210.55,2456789,2,5123456,623145.78,1123456.44,2894567,3,8450000,523145.66,1023456.77,2456789,2,1,0,0,0,210,350,0.65,1.10,1,22,9.54,10.11,120.45,0,0,0,0,1,0,0,1,0,10.45,10.50,10.40,210,0,1,0,0,0,0,7,95,10,150,18000,180,4,20,0,0,0,0,0,0,0,0]
}
    </textarea>

    <button onclick="predict()">Analyze Traffic</button>

    <div id="result"></div>

    <h3> Live Logs</h3>
    <div id="logs"></div>

</div>

<script>
let total = 0;
let attacks = 0;
let normal = 0;

async function predict() {
    const input = document.getElementById("inputData").value;
    const resultDiv = document.getElementById("result");

    try {
        resultDiv.innerHTML = " Analyzing...";

        const parsedData = JSON.parse(input);

        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(parsedData)
        });

        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = "❌ " + data.error;
            return;
        }

        total++;
        document.getElementById("total").innerText = total;

        if (data.prediction === 1) {
            attacks++;
            document.getElementById("attacks").innerText = attacks;
            resultDiv.innerHTML = " Attack Detected! <br> Confidence: " + data.confidence;
            addLog(" Attack detected");
        } else {
            normal++;
            document.getElementById("normal").innerText = normal;
            resultDiv.innerHTML = " Normal Traffic <br> Confidence: " + data.confidence;
            addLog(" Normal traffic");
        }

    } catch (error) {
        console.error(error);
        resultDiv.innerHTML = "Failed to connect to API";
    }
}

function addLog(message) {
    const logs = document.getElementById("logs");
    const time = new Date().toLocaleTimeString();

    logs.innerHTML = `[${time}] ${message} <br>` + logs.innerHTML;
}
</script>

</body>
</html>
"""
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

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
    app.run()