# =========================================
# ui.py
# Journey prediction 
# =========================================

import streamlit as st
from api import predict_journey
from ocr_api import extract_journey_from_ticket   # OCR pipeline


st.set_page_config(page_title="Nagpur Metro Journey Crowd Prediction")
st.title("🚇 Nagpur Metro Journey Crowd Prediction")



# -----------------------------
# Time Dropdown
# -----------------------------
def generate_times():
    times = []
    for h in range(8, 23):
        for m in [0, 20, 40]:
            times.append(f"{h:02d}:{m:02d}")
    times.append("23:00")
    return times


# -----------------------------
# Stations
# -----------------------------
AQUA = [
    "Prajapati Nagar", "Vaishno Devi Square", "Ambedkar Square",
    "Telephone Exchange", "Chitar Oli Square", "Agrasen Square",
    "Dosar Vaisya Square", "Nagpur Railway Station", "Cotton Market",
    "Sitabuldi (EW)", "Jhansi Rani Square", "Institution of Engineers",
    "Shankar Nagar Square", "LAD Square", "Dharampeth College",
    "Subhash Nagar", "Rachana Ring Road", "Vasudev Nagar",
    "Bansi Nagar", "Lokmanya Nagar"
]

ORANGE = [
    "Automotive Square", "Nari Road", "Indora Square", "Kadbi Square",
    "Gaddi Godam Square", "Kasturchand Park", "Zero Mile Freedom Park",
    "Sitabuldi (NS)", "Congress Nagar", "Rahate Colony", "Ajni Square",
    "Chhatrapati Square", "Jaiprakash Nagar", "Ujjwal Nagar",
    "Airport", "Airport South", "New Airport", "Khapri"
]

ALL_STATIONS = sorted(set(AQUA + ORANGE))


# ==================================================
# SECTION 1 — MANUAL JOURNEY PREDICTION (UNCHANGED)
# ==================================================
st.subheader("🧭 Plan Your Journey (Manual)")

source = st.selectbox("Source Station", ALL_STATIONS)
destination = st.selectbox("Destination Station", ALL_STATIONS)
arrival_time = st.selectbox("Arrival Time", generate_times())
day_type = st.selectbox("Day Type", ["Weekday", "Weekend"])

if st.button("Predict Crowd for Selected Train"):

    result = predict_journey(
        source,
        destination,
        arrival_time,
        day_type
    )

    st.subheader("🚆 Journey Prediction")

    if result["type"] == "Direct":
        st.success("Direct Journey")
        st.markdown(f"**Source Crowd:** 🚦 {result['source_crowd']}")
    else:
        st.warning("Interchange at Sitabuldi")
        st.markdown(f"**Source Crowd:** 🚦 {result['source_crowd']}")
        st.markdown(f"**Interchange Crowd (Sitabuldi):** 🚦 {result['interchange_crowd']}")

    st.markdown(f"**Estimated Travel Time:** 🕒 {result['travel_time']} minutes")


# ==================================================
# SECTION 2 — OCR TICKET PREDICTION (SEPARATE)
# ==================================================
# ---------------- OCR SECTION ----------------
# ---------------- OCR SECTION ----------------
st.divider()
st.subheader("📸 OCR Journey Prediction")

ticket = st.file_uploader("Upload Ticket", type=["png", "jpg", "jpeg"])

# ✅ Initialize variables (IMPORTANT)
src = dest = time_ocr = raw = None

if ticket:
    with open("ticket.png", "wb") as f:
        f.write(ticket.getbuffer())

    src, dest, time_ocr, raw = extract_journey_from_ticket("ticket.png")

    if not src or not dest or not time_ocr:
        st.error("OCR failed to extract journey details")
        st.text(raw)

    else:
        st.success("OCR Journey Extracted")
        st.write("Source:", src)
        st.write("Destination:", dest)
        st.write("Time:", time_ocr)

        day_type_ocr = st.selectbox(
            "Day Type",
            ["Weekday", "Weekend"],
            key="ocr_day"
        )

        if st.button("Predict OCR Journey"):
            result = predict_journey(
                src,
                dest,
                time_ocr,
                day_type_ocr
            )

            st.subheader("🚆 Journey Prediction")

            if result["type"] == "Direct":
                st.success("Direct Journey")
                st.markdown(f"**Source Crowd:** 🚦 {result['source_crowd']}")
            else:
                st.warning("Interchange at Sitabuldi")
                st.markdown(f"**Source Crowd:** 🚦 {result['source_crowd']}")
                st.markdown(
                    f"**Interchange Crowd (Sitabuldi):** 🚦 {result['interchange_crowd']}"
                )

            st.markdown(
                f"**Estimated Travel Time:** 🕒 {result['travel_time']} minutes"
            )

