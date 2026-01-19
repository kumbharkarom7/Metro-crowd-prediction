# =========================================
# api.py
# Backend with proper interchange handling
# =========================================

import pickle
import pandas as pd


# -----------------------------
# Load model & encoders
# -----------------------------
model = pickle.load(open("metro_crowd_model.pkl", "rb"))
label_encoders = pickle.load(open("label_encoders.pkl", "rb"))


# -----------------------------
# Metro Lines
# -----------------------------
ORANGE_LINE = [
    "Automotive Square", "Nari Road", "Indora Square", "Kadbi Square",
    "Gaddi Godam Square", "Kasturchand Park", "Zero Mile Freedom Park",
    "Sitabuldi (NS)", "Congress Nagar", "Rahate Colony", "Ajni Square",
    "Chhatrapati Square", "Jaiprakash Nagar", "Ujjwal Nagar",
    "Airport", "Airport South", "New Airport", "Khapri"
]

AQUA_LINE = [
    "Prajapati Nagar", "Vaishno Devi Square", "Ambedkar Square",
    "Telephone Exchange", "Chitar Oli Square", "Agrasen Square",
    "Dosar Vaisya Square", "Nagpur Railway Station", "Cotton Market",
    "Sitabuldi (EW)", "Jhansi Rani Square", "Institution of Engineers",
    "Shankar Nagar Square", "LAD Square", "Dharampeth College",
    "Subhash Nagar", "Rachana Ring Road", "Vasudev Nagar",
    "Bansi Nagar", "Lokmanya Nagar"
]


# -----------------------------
# Time → Slot
# -----------------------------
def map_time_to_slot(hour):
    if 8 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 16:
        return "Afternoon"
    elif 16 <= hour < 20:
        return "Evening Peak"
    else:
        return "Night"


# -----------------------------
# Ticket Estimation (System-side)
# -----------------------------
def estimate_ticket_count(station, time_slot, day_type):
    base = 60

    if "Sitabuldi" in station or "Nagpur Railway Station" in station:
        base += 120
    elif station in ["Agrasen Square", "Subhash Nagar", "Airport"]:
        base += 80
    else:
        base += 40

    if time_slot == "Morning":
        base += 60
    elif time_slot == "Evening Peak":
        base += 80
    elif time_slot == "Night":
        base -= 20

    if day_type == "Weekend":
        base -= 20

    return max(20, min(base, 300))


# -----------------------------
# Travel Time Estimation
# -----------------------------
def estimate_travel_time(source, destination):

    # Same station
    if source == destination:
        return 0

    # Aqua → Aqua
    if source in AQUA_LINE and destination in AQUA_LINE:
        return abs(AQUA_LINE.index(source) - AQUA_LINE.index(destination)) * 2

    # Orange → Orange
    if source in ORANGE_LINE and destination in ORANGE_LINE:
        return abs(ORANGE_LINE.index(source) - ORANGE_LINE.index(destination)) * 2

    # Aqua → Orange (via Sitabuldi)
    if source in AQUA_LINE and destination in ORANGE_LINE:
        aqua_dist = abs(AQUA_LINE.index(source) - AQUA_LINE.index("Sitabuldi (EW)"))
        orange_dist = abs(ORANGE_LINE.index(destination) - ORANGE_LINE.index("Sitabuldi (NS)"))
        return (aqua_dist + orange_dist) * 2 + 5

    # Orange → Aqua (via Sitabuldi)
    if source in ORANGE_LINE and destination in AQUA_LINE:
        orange_dist = abs(ORANGE_LINE.index(source) - ORANGE_LINE.index("Sitabuldi (NS)"))
        aqua_dist = abs(AQUA_LINE.index(destination) - AQUA_LINE.index("Sitabuldi (EW)"))
        return (orange_dist + aqua_dist) * 2 + 5

    # Safety fallback
    return None


# -----------------------------
# Crowd Prediction (WITH INTERCHANGE)
# -----------------------------
def predict_journey(source, destination, arrival_time, day_type):
    hour = int(arrival_time.split(":")[0])
    time_slot = map_time_to_slot(hour)

    results = {}

    # SAME LINE
    if (source in AQUA_LINE and destination in AQUA_LINE) or \
       (source in ORANGE_LINE and destination in ORANGE_LINE):

        route = "Aqua Line (East-West)" if source in AQUA_LINE else "Orange Line (North-South)"
        ticket_count = estimate_ticket_count(source, time_slot, day_type)

        df = pd.DataFrame([{
            "route_id": route,
            "station_name": source,
            "day_type": day_type,
            "time_slot": time_slot,
            "ticket_count_5min": ticket_count
        }])

        for col in ["route_id", "station_name", "day_type", "time_slot"]:
            df[col] = label_encoders[col].transform(df[col])

        results["type"] = "Direct"
        results["source_crowd"] = model.predict(df)[0]

    # INTERCHANGE JOURNEY
    else:
        # Source crowd
        source_route = "Aqua Line (East-West)" if source in AQUA_LINE else "Orange Line (North-South)"
        source_ticket = estimate_ticket_count(source, time_slot, day_type)

        df_source = pd.DataFrame([{
            "route_id": source_route,
            "station_name": source,
            "day_type": day_type,
            "time_slot": time_slot,
            "ticket_count_5min": source_ticket
        }])

        # Interchange crowd
        interchange_station = "Sitabuldi (EW)" if source in AQUA_LINE else "Sitabuldi (NS)"
        interchange_route = "Aqua Line (East-West)" if interchange_station.endswith("EW") else "Orange Line (North-South)"
        interchange_ticket = estimate_ticket_count(interchange_station, time_slot, day_type)

        df_inter = pd.DataFrame([{
            "route_id": interchange_route,
            "station_name": interchange_station,
            "day_type": day_type,
            "time_slot": time_slot,
            "ticket_count_5min": interchange_ticket
        }])

        for df in [df_source, df_inter]:
            for col in ["route_id", "station_name", "day_type", "time_slot"]:
                df[col] = label_encoders[col].transform(df[col])

        results["type"] = "Interchange"
        results["source_crowd"] = model.predict(df_source)[0]
        results["interchange_crowd"] = model.predict(df_inter)[0]

    results["travel_time"] = estimate_travel_time(source, destination)
    return results
