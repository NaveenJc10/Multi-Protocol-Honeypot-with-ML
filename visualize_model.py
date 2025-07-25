import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv('encoded_honeypot_logs.csv')

# Labeling attack_type
def label_attack(row):
    if row['action'] == 'login' and row.get('status') == 'failed':
        return 'brute_force'
    elif row['action'] == 'login' and "' OR" in str(row.get('password', '')):
        return 'sqli'
    elif row['action'] == 'connection' and 'FROM:' in str(row):
        return 'spoofing'
    else:
        return 'other'

df['attack_type'] = df.apply(label_attack, axis=1)

# Clean up features
features = df.drop(columns=['attack_type', 'timestamp', 'src_ip', 'dest_ip', 'username', 'password', 'data_command', 'data_arg'], errors='ignore')
target = df['attack_type']

# Label encode
for col in features.columns:
    if features[col].dtype == 'object':
        le = LabelEncoder()
        features[col] = le.fit_transform(features[col].astype(str))

# Split
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict
y_pred = clf.predict(X_test)

# Confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

# Feature importance
importances = clf.feature_importances_
feature_names = features.columns

plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=feature_names)
plt.title("Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()

