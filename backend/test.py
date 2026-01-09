import joblib

model = joblib.load("model/knn_model.pkl")
scaler = joblib.load("model/scaler.pkl")

print(model)
print(scaler)
