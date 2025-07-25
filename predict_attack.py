import json
import pandas as pd
import joblib

# Load trained classifier with encoder
clf = joblib.load("attack_classifier.pkl")

# ✅ Sample log entry (you can replace this with real-time data later)
log_entry = {
    "action": "login",
    "dest_ip": "0.0.0.0",
    "dest_port": 8080,
    "server": "http_server",
    "src_ip": "127.0.0.1",
    "src_port": 40010,
    "status": "failed",
    "timestamp": "2025-06-12T04:50:39.875655",
    "password": "' OR '1'='1",
    "username": "admin",
    "data_arg": None,
    "data_command": None,
    "data_data": None
}

# 🛠 Combine into 'data' field expected by model
log_entry["data"] = str(log_entry.get("data_arg", "")) + "|" + str(log_entry.get("data_command", "")) + "|" + str(log_entry.get("data_data", ""))

# Remove raw data_* fields if model wasn't trained on them
log_entry.pop("data_arg", None)
log_entry.pop("data_command", None)
log_entry.pop("data_data", None)

# Define final required fields (based on encoded CSV + model)
required_fields = [
    "action", "dest_ip", "dest_port", "server", "src_ip", "src_port",
    "status", "timestamp", "password", "username", "data"
]

# Fill missing fields with None
for field in required_fields:
    if field not in log_entry:
        log_entry[field] = None

# Create DataFrame and predict
df = pd.DataFrame([log_entry])
prediction = clf.predict(df)[0]
print(f"🚨 Predicted Attack Type: {prediction}")

