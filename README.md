# Metro-crowd-prediction
# 🚇 Nagpur Metro Crowd Prediction System

An AI/ML-based Smart City application to predict real-time crowd levels in Nagpur Metro trains using journey data and OCR-based ticket analysis.

---

## 📌 Overview
The Nagpur Metro Crowd Prediction System predicts metro crowd levels (LOW, MEDIUM, HIGH) for upcoming journeys.  
It supports both manual journey planning and OCR-based ticket prediction, with proper interchange handling at Sitabuldi station.

This project is designed for academic, smart city, and intelligent transport system use cases.

---

## 🎯 Features
- Real-time crowd level prediction
- Manual journey input
- OCR-based ticket journey extraction
- Interchange detection at Sitabuldi
- Travel time estimation
- Machine learning–based prediction
- Confusion matrix visualization

---

## 🏗️ System Architecture
Flow:
1. User enters journey details manually or uploads a ticket image
2. OCR extracts journey details from ticket (OCR mode)
3. Inputs are normalized and validated
4. Backend applies interchange and routing logic
5. ML model predicts crowd level
6. UI displays crowd level and travel time

---

## 🛠️ Tech Stack
- Python
- Scikit-learn (Random Forest)
- Tesseract OCR
- Streamlit
- Matplotlib & Seaborn

---


---

## 📊 Dataset
Synthetic yet realistic Nagpur Metro dataset covering Aqua and Orange lines.

Features:
- route_id
- station_name
- day_type
- time_slot
- ticket_count_5min

Target:
- crowd_level (LOW / MEDIUM / HIGH)

Note: Capacity and occupancy are excluded to avoid data leakage.

---

## 🧠 Machine Learning Model
- Algorithm: Random Forest Classifier
- Accuracy: ~93–95%
- Evaluation: Accuracy, Precision, Recall, Confusion Matrix


---

## 🧾 OCR-Based Prediction
- Upload a Nagpur Metro ticket image
- OCR extracts source, destination, and time
- Fuzzy matching handles OCR noise
- Same ML model is reused for prediction

---

## 🧑‍🏫 Use Cases
- Passenger journey planning
- Metro congestion monitoring
- Smart city analytics
- Academic and final-year projects

---

## 🔮 Future Scope
- Real AFC data integration
- LSTM-based time-series forecasting
- Live dashboard with maps
- Mobile application support

---

## 📜 License
This project is intended for educational and academic purposes.





