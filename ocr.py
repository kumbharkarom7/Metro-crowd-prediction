# =========================================
# ocr.py
# Layout-aware OCR for Nagpur Metro ticket
# =========================================

import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_ticket_text(image_path):
    img = Image.open(image_path).convert("L")
    text = pytesseract.image_to_string(img, config="--psm 6")
    return text


import re
from difflib import get_close_matches

def extract_from_to_time(text):
    text_clean = " ".join(text.split()).lower()

    # Normalize OCR garbage
    replacements = {
        "ngr": "nagar",
        "subhas": "subhash",
        "rallway": "railway",
        "railway statlon": "railway station"
    }
    for k, v in replacements.items():
        text_clean = text_clean.replace(k, v)

    STATIONS = [
        "subhash nagar",
        "nagpur railway station",
        "sitabuldi",
        "agrassen square",
        "cotton market",
        "airport",
        "khapri",
        "ajni square"
    ]

    words = text_clean.split()

    found = []
    for station in STATIONS:
        match = get_close_matches(station, text_clean.split(), n=1, cutoff=0.6)
        if station in text_clean or match:
            found.append(station)

    # Remove duplicates while keeping order
    found = list(dict.fromkeys(found))

    if len(found) < 2:
        return None

    source = found[0].title()
    destination = found[1].title()

    time_match = re.search(r"\d{1,2}:\d{2}:\d{2}\s?(am|pm)", text_clean)
    if not time_match:
        return None

    return {
        "source": source,
        "destination": destination,
        "time": time_match.group(0)
    }
