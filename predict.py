# =========================================
# Nagpur Metro Crowd Prediction
# Prediction Script
# =========================================

import pickle
import pandas as pd


# -----------------------------
# 1. Load Model & Encoders
# -----------------------------
MODEL_PATH = "metro_crowd_model.pkl"
ENCODER_PATH = "label_encoders.pkl"

model = pickle.load(open(MODEL_PATH, "rb"))
label_encoders = pickle.load(open(ENCODER_PATH, "rb"))

print("✅ Model and encoders loaded successfully!")


# -----------------------------
# 2. Time Mapping Function
# -----------------------------
def map_time_to_slot(hour, minute):
    """
    Maps exact time to coarse time_slot
    """
    if 8 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 16:
        return "Afternoon"
    elif 16 <= hour < 20:
        return "Evening Peak"
    else:
        return "Night"


# -----------------------------
# 3. Prediction Function
# -----------------------------
def predict_crowd(
    route_id,
    station_name,
    day_type,
    hour,
    minute,
    ticket_count_5min
):
    """
    Predict crowd level for upcoming metro
    """

    # Convert exact time → time_slot
    time_slot = map_time_to_slot(hour, minute)

    # Create input dataframe
    input_data = pd.DataFrame([{
        "route_id": route_id,
        "station_name": station_name,
        "day_type": day_type,
        "time_slot": time_slot,
        "ticket_count_5min": ticket_count_5min
    }])

    # Encode categorical features
    for col in ["route_id", "station_name", "day_type", "time_slot"]:
        input_data[col] = label_encoders[col].transform(input_data[col])

    # Predict
    prediction = model.predict(input_data)[0]

    return prediction


# -----------------------------
# 4. EXAMPLE USAGE
# -----------------------------
if __name__ == "__main__":

    # 🔹 Example: User wants to go from Chitar Oli → Airport
    route_id = "Aqua Line (East-West)"
    station_name = "Chitar Oli Square"
    day_type = "Weekday"

    # User selects arrival time from dropdown
    hour = 14      # 2 PM
    minute = 20    # 2:20 PM

    # Recent ticket scans (last 5 minutes)
    ticket_count_5min = 135

    crowd = predict_crowd(
        route_id,
        station_name,
        day_type,
        hour,
        minute,
        ticket_count_5min
    )

    print("\n🚇 Crowd Prediction Result")
    print("--------------------------")
    print("Route       :", route_id)
    print("Station     :", station_name)
    print("Arrival Time: 14:20")
    print("Crowd Level :", crowd)
