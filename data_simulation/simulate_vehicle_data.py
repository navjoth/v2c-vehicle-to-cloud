import csv
import json
import random
from datetime import datetime

def generate_data_point():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "speed": round(random.uniform(0, 140), 2),               # km/h
        "rpm": round(random.uniform(800, 6000), 0),              # revolutions per minute
        "fuel_rate": round(random.uniform(2, 20), 2),            # liters/hour
        "brake_pressure": round(random.uniform(0, 100), 2),      # percentage
        "throttle_position": round(random.uniform(0, 100), 2)    # percentage
    }

def write_csv(filename, num_points=100):
    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(generate_data_point().keys()))
        writer.writeheader()
        for _ in range(num_points):
            writer.writerow(generate_data_point())

def write_json(filename, num_points=100):
    with open(filename, 'w') as f:
        data = [generate_data_point() for _ in range(num_points)]
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    write_csv("vehicle_log.csv")
    write_json("vehicle_log.json")
    print("Generated vehicle_log.csv and vehicle_log.json with 100 entries each.")
