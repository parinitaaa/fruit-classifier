from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

# Load saved model & scaler
knn = joblib.load("model/knn_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# Load lookup table
fruits = pd.read_table("data/fruitdata.txt")
lookup_fruit_name = dict(
    zip(fruits.fruit_label.unique(), fruits.fruit_name.unique())
)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        new_fruit = pd.DataFrame(
            [[
                float(data["height"]),
                float(data["width"]),
                float(data["mass"]),
                float(data["color_score"])
            ]],
            columns=["height", "width", "mass", "color_score"]
        )

        new_fruit_scaled = scaler.transform(new_fruit)
        fruit_label = knn.predict(new_fruit_scaled)[0]
        fruit_name = lookup_fruit_name[fruit_label]
        proba = knn.predict_proba(new_fruit_scaled)
        confidence = float(max(proba[0]))
       

        return jsonify({
            "fruit": fruit_name,
            "model": "KNN",
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
