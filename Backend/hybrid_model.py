from model_rf import predict_rf
from model_if import predict_if

def hybrid_predict(features):
    rf_result = predict_rf(features)
    if_result = predict_if(features)

    # Decision logic
    if rf_result == 1:
        return "Known Attack"
    elif if_result == -1:
        return "Unknown Anomaly"
    else:
        return "Normal"