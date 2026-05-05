import joblib
import numpy as np

# Load models once
rf_model = joblib.load("rf_model.pkl")

# (Optional) load isolation forest if you have it
# if_model = joblib.load("if_model.pkl")


def preprocess_input(data):
    """
    Convert input JSON to model format
    Modify this based on your features
    """
    return np.array(data).reshape(1, -1)


def predict_rf(features):
    return rf_model.predict(features)[0]


def hybrid_predict(data):
    features = preprocess_input(data)

    rf_result = predict_rf(features)

    # Example hybrid logic
    # if_result = if_model.predict(features)

    if rf_result == 1:
        return "Known Attack"
    else:
        return "Normal"