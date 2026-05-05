from sklearn.ensemble import IsolationForest
import numpy as np

# Train once (or load if saved)
iso_model = IsolationForest(contamination=0.1)
iso_model.fit(np.random.rand(100, 2))  # replace with real training later

def predict_if(features):
    pred = iso_model.predict([features])[0]
    return pred  # 1 = normal, -1 = anomaly
