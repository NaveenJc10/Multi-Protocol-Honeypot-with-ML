import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import json

# Load encoded data and model
df = pd.read_csv("encoded_honeypot_logs.csv")
model = joblib.load("attack_classifier.pkl")

X = df.drop(columns=["attack_type"])
y = df["attack_type"]

# Train-test split for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Predict on test
y_pred = model.predict(X_test)

# Generate classification report
report = classification_report(y_test, y_pred, output_dict=True)
text_report = classification_report(y_test, y_pred)

# Save to text file
with open("model_metrics.txt", "w") as f:
    f.write(text_report)

# Insert into HTML report at the top
try:
    with open("honeypot_report.html", "r") as f:
        html_content = f.read()

    metrics_html = f"""
    <div style="padding:10px; border:2px solid #4CAF50; margin-bottom:20px;">
        <h3>📊 Model Evaluation Metrics</h3>
        <pre>{json.dumps(report, indent=2)}</pre>
    </div>
    """
    updated_html = html_content.replace("<body>", f"<body>{metrics_html}", 1)

    with open("honeypot_report.html", "w") as f:
        f.write(updated_html)

    print("✅ Evaluation metrics added to honeypot_report.html and saved in model_metrics.txt")
except Exception as e:
    print(f"⚠ Could not update HTML: {e}")

print("\n=== Classification Report ===\n")
print(text_report)

