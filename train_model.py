# ================================
# Nagpur Metro Crowd Prediction
# Model Training Script
# ================================

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


# ----------------
# 1. Load Dataset
# ----------------
DATA_PATH = "Nagpur_Metro_Dataset.csv"
df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)


# ---------------------------------
# 2. Select Features & Target
# ---------------------------------
# IMPORTANT:
# Do NOT include capacity or occupancy to avoid leakage
features = [
    "route_id",
    "station_name",
    "day_type",
    "time_slot",
    "ticket_count_5min"
]

target = "crowd_level"

X = df[features].copy()   # .copy() fixes SettingWithCopyWarning
y = df[target]


# ---------------------------------
# 3. Encode Categorical Features
# ---------------------------------
label_encoders = {}

categorical_cols = [
    "route_id",
    "station_name",
    "day_type",
    "time_slot"
]

for col in categorical_cols:
    le = LabelEncoder()
    X.loc[:, col] = le.fit_transform(X[col])
    label_encoders[col] = le


# ---------------------------------
# 4. Train-Test Split
# ---------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)


# ---------------------------------
# 5. Train Random Forest Model
# ---------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=10,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ---------------------------------
# 6. Evaluate Model
# ---------------------------------
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", round(accuracy, 4))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# ---------------------------------
# 7. Save Model & Encoders
# ---------------------------------
pickle.dump(model, open("metro_crowd_model.pkl", "wb"))
pickle.dump(label_encoders, open("label_encoders.pkl", "wb"))

print("\n✅ Model & encoders saved successfully!")
