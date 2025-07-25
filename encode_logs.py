import json
import pandas as pd

with open("honeypot_logs.json", "r") as f:
    logs = []
    for line in f:
        if not line.strip().startswith("{"):
            continue
        try:
            entry = json.loads(line)
            if "action" not in entry:
                continue
            # Add simple attack_type tagging based on logic
            action = entry.get("action", "").lower()
            attack_type = "other"
            if action == "login" and entry.get("status") == "failed":
                attack_type = "brute_force"
            elif action == "login" and entry.get("status") == "success":
                attack_type = "brute_force"
            elif "' or '" in str(entry.get("password", "")).lower() or "1=1" in str(entry.get("password", "")).lower():
                attack_type = "sqli"
            elif entry.get("server") == "smtp_server":
                attack_type = "spoofing"

            entry["attack_type"] = attack_type
            logs.append(entry)
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(logs)
df.to_csv("encoded_honeypot_logs.csv", index=False)
print("✅ Encoded dataset with attack_type saved as 'encoded_honeypot_logs.csv'")

