import joblib

rf_model = joblib.load("rf_model.pkl")

def predict_rf(features):
    pred = rf_model.predict([features])[0]
    return pred