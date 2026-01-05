from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# -------------------------
# 1️⃣ Load and prepare dataset
# -------------------------
fruits = pd.read_table('data/fruitdata.txt') 

# Features and labels
X = fruits[['height', 'width', 'mass', 'color_score']]
Y = fruits['fruit_label']

# Scale features so KNN works properly
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_scaled, Y)

# Map numeric labels to fruit names
lookup_fruit_name = dict(zip(fruits.fruit_label.unique(), fruits.fruit_name.unique()))

# -------------------------
# 2️⃣ API endpoint
# -------------------------
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        # Extract features from JSON
        height = float(data['height'])
        width = float(data['width'])
        mass = float(data['mass'])
        color_score = float(data['color_score'])

        # Put into DataFrame
        new_fruit = pd.DataFrame([[height, width, mass, color_score]], columns=X.columns)

        # Scale new input
        new_fruit_scaled = scaler.transform(new_fruit)

        # Predict label
        fruit_label = knn.predict(new_fruit_scaled)[0]
        fruit_name = lookup_fruit_name[fruit_label]

        # Return JSON response
        return jsonify({'fruit': fruit_name})

    except Exception as e:
        return jsonify({'error': str(e)})

# -------------------------
# 3️⃣ Run app
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
whatr