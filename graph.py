# ======================================
# graph.py
# Confusion Matrix Visualization
# ======================================

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("Nagpur_Metro_Dataset.csv")

# -----------------------------
# Load model & encoders
# -----------------------------
model = pickle.load(open("metro_crowd_model.pkl", "rb"))
label_encoders = pickle.load(open("label_encoders.pkl", "rb"))

# -----------------------------
# Features & target
# -----------------------------
X = df[[
    "route_id",
    "station_name",
    "day_type",
    "time_slot",
    "ticket_count_5min"
]]

y = df["crowd_level"]

# -----------------------------
# Encode categorical columns
# -----------------------------
for col in ["route_id", "station_name", "day_type", "time_slot"]:
    X[col] = label_encoders[col].transform(X[col])

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# -----------------------------
# Prediction
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Confusion Matrix
# -----------------------------
cm = confusion_matrix(y_test, y_pred)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["HIGH", "LOW", "MEDIUM"],
    yticklabels=["HIGH", "LOW", "MEDIUM"]
)

plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix – Metro Crowd Prediction Model")
plt.tight_layout()
plt.show()
