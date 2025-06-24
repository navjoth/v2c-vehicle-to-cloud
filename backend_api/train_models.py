import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
import joblib

# Load the simulated data
df = pd.read_json('../data_simulation/vehicle_log.json')

# --------------------------
# Model 1: Fuel Efficiency Predictor
# --------------------------

X_fuel = df[["speed", "rpm", "throttle_position"]]
y_fuel = df["fuel_rate"]

fuel_model = RandomForestRegressor(n_estimators=100, random_state=42)
fuel_model.fit(X_fuel, y_fuel)

joblib.dump(fuel_model, "fuel_efficiency_model.pkl")
print("✅ Saved fuel_efficiency_model.pkl")

# --------------------------
# Model 2: Driver Behavior Classifier
# --------------------------

X_driver = df[["speed", "brake_pressure", "throttle_position"]]

# KMeans will create 3 clusters: 0, 1, 2 (we'll interpret later)
driver_model = KMeans(n_clusters=3, random_state=42)
driver_model.fit(X_driver)

joblib.dump(driver_model, "driver_behavior_model.pkl")
print("✅ Saved driver_behavior_model.pkl")
