from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

rf = joblib.load("model/rf_model.pkl")

fruits = pd.read_table("data/fruitdata.txt")
lookup_fruit_name = dict(zip(fruits.fruit_label.unique(), fruits.fruit_name.unique()))

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

        fruit_label = rf.predict(new_fruit)[0]
        fruit_name = lookup_fruit_name[fruit_label]

        proba = rf.predict_proba(new_fruit)
        confidence = float(max(proba[0]))
       

        return jsonify({
            "fruit": fruit_name,
            "model": "Random  Forest",
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
