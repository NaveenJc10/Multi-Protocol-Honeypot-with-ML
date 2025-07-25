import json
import time
import joblib
import numpy as np
import pandas as pd

FEATURES = ['action', 'dest_ip', 'dest_port', 'server', 'src_ip', 'src_port',
            'status', 'timestamp', 'password', 'username', 'data']

model = joblib.load("attack_classifier.pkl")

def flatten_data_field(data):
    # If data is a dict, flatten to a string; otherwise, keep as is or make string
    if isinstance(data, dict):
        return json.dumps(data)
    return str(data) if data is not None else ""

with open("honeypot_logs.json") as f:
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.2)
            continue
        try:
            entry = json.loads(line)
            # Build row for model
            row = {}
            for key in FEATURES:
                val = entry.get(key, "")
                # Special handling for 'data'
                if key == "data":
                    val = flatten_data_field(val)
                row[key] = val
            df = pd.DataFrame([row])
            # Predict (your model may need encoder, adjust here if needed)
            pred = model.predict(df)[0]
            print(f"Prediction: {pred} | Log: {row}")
        except Exception as e:
            print(f"[!] Skipping line due to error: {e}")

