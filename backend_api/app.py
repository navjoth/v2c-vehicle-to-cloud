from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load pre-trained models
fuel_model = joblib.load("fuel_efficiency_model.pkl")
driver_model = joblib.load("driver_behavior_model.pkl")

def interpret_driver_cluster(cluster_id):
    labels = {
        0: "Efficient",
        1: "Average",
        2: "Aggressive"
    }
    return labels.get(cluster_id, "Unknown")

@app.route("/", methods=["GET"])
def index():
    return "✅ V2C ML Backend is running!"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        json_data = request.get_json()
        df = pd.DataFrame(json_data)

        # Fuel Efficiency Prediction
        X_fuel = df[["speed", "rpm", "throttle_position"]]
        predicted_fuel = fuel_model.predict(X_fuel)
        avg_predicted_fuel = np.mean(predicted_fuel)
        actual_fuel = np.mean(df["fuel_rate"])
        efficiency_gap = actual_fuel - avg_predicted_fuel

        # Driver Behavior Classification
        X_driver = df[["speed", "brake_pressure", "throttle_position"]]
        cluster_labels = driver_model.predict(X_driver)
        most_common = np.bincount(cluster_labels).argmax()
        driver_type = interpret_driver_cluster(most_common)

        return jsonify({
            "driver_type": driver_type,
            "actual_avg_fuel_rate": round(actual_fuel, 2),
            "predicted_avg_fuel_rate": round(avg_predicted_fuel, 2),
            "efficiency_gap": round(efficiency_gap, 2),
            "insights": [
                f"Driver type classified as: {driver_type}",
                f"Fuel usage is {'higher' if efficiency_gap > 0 else 'efficient'} compared to prediction"
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
