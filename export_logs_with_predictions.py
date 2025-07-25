import pandas as pd
import json
import joblib

# === 1. LOAD LOGS SAFELY ===
logs = []
with open("honeypot_logs.json") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            logs.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"[!] Skipping invalid line: {line[:50]}... ({e})")

if not logs:
    print("[!] No valid log entries found in honeypot_logs.json")
    exit(1)

df = pd.DataFrame(logs).fillna("")

# === 2. STRINGIFY ANY DICT COLUMNS ===
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, dict)).any():
        df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)

# === 3. LOAD ML MODEL & PREDICT ===
model = joblib.load("attack_classifier.pkl")
feature_columns = model.feature_names_in_

# Only use columns that exist in df
used_features = [col for col in feature_columns if col in df.columns]
missing_features = [col for col in feature_columns if col not in df.columns]
for col in missing_features:
    df[col] = ""  # Fill missing columns with empty string (or default value)

df["predicted_attack_type"] = model.predict(df[feature_columns])

# === 4. EXPORT ===
df.to_csv("exported_logs_with_predictions.csv", index=False)
with open("exported_logs_with_predictions.json", "w") as f:
    json.dump(df.to_dict(orient="records"), f, indent=4)

print("✅ Export complete: 'exported_logs_with_predictions.csv' & 'exported_logs_with_predictions.json'")

