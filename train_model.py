import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("encoded_honeypot_logs.csv")

# Drop rows with missing target
df = df.dropna(subset=["attack_type"])

# Separate features and labels
X = df.drop("attack_type", axis=1)
y = df["attack_type"]

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

# Preprocessor for encoding categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ],
    remainder="passthrough"
)

# Build pipeline
clf = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
print("✅ Accuracy:", clf.score(X_test, y_test))
print(classification_report(y_test, y_pred))

# Save the entire pipeline including encoder + model
joblib.dump(clf, "attack_classifier.pkl")
print("✅ Model with encoder saved as 'attack_classifier.pkl'")

