import json
import requests

with open('honeypot_logs.json') as f:
    logs = [json.loads(line) for line in f if line.strip() and line.strip().startswith('{')]

for log in logs:
    r = requests.post('http://localhost:9200/honeypot/_doc', json=log)
    print(f"Indexed log: {r.status_code}")

