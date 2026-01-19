from ocr import extract_ticket_text, extract_from_to_time

def normalize_time(t):
    try:
        t = t.lower().strip()
        time_part, meridian = t.split()
        h, m, s = map(int, time_part.split(":"))

        if meridian == "pm" and h < 12:
            h += 12
        if meridian == "am" and h == 12:
            h = 0

        return f"{h:02d}:{m:02d}"
    except:
        return None


def extract_journey_from_ticket(image_path):
    text = extract_ticket_text(image_path)

    data = extract_from_to_time(text)

    # 🔴 THIS LINE IS MANDATORY
    if data is None:
        return None, None, None, text

    # 🔴 ALSO MANDATORY
    if (
        "source" not in data or
        "destination" not in data or
        "time" not in data
    ):
        return None, None, None, text

    t = normalize_time(data["time"])
    if t is None:
        return None, None, None, text

    return data["source"], data["destination"], t, text
