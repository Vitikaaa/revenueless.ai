import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load data
df = pd.read_csv("data/transactions.csv")

# We only care about failed transactions
failed = df[df["status"] == "failed"].copy()

# Create a synthetic recovery label for our prototype
# Higher chance of recovery if customer has tried multiple times
# and has previously completed payments.
failed["recovery"] = (
    (
        (failed["retry_count"] >= 1) &
        (failed["checkout_started"] == 1)
    )
    |
    (failed["amount"] < failed["amount"].median())
).astype(int)

features = [
    "amount",
    "retry_count",
    "hour",
    "checkout_started"
]

X = failed[features]
y = failed["recovery"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("\n===== REVENUELENS RECOVERY MODEL =====")
print(classification_report(y_test, predictions))

# Save model
os.makedirs("ml/models", exist_ok=True)

joblib.dump(
    model,
    "ml/models/recovery_model.pkl"
)

print("Model saved successfully!")