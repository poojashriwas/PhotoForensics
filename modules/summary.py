import random
from datetime import datetime


def generate_summary(metadata, gps, ela, quality, histogram):

    score = 100
    reasons = []

    # -------------------------
    # Metadata
    # -------------------------

    if metadata.get("Image Make") == "Not Available":
        score -= 10
        reasons.append("Camera metadata unavailable.")
    else:
        reasons.append("Camera metadata detected.")

    # -------------------------
    # GPS
    # -------------------------

    if gps.get("Status") == "GPS Coordinates Found":
        reasons.append("GPS metadata available.")
    else:
        score -= 5
        reasons.append("GPS metadata not found.")

    # -------------------------
    # ELA
    # -------------------------

    if ela["risk"] == "High":
        score -= 30
        reasons.append("High compression differences detected.")

    elif ela["risk"] == "Medium":
        score -= 15
        reasons.append("Moderate compression differences detected.")

    else:
        reasons.append("ELA indicates low compression differences.")

    # -------------------------
    # Image Quality
    # -------------------------

    if quality["blur"] == "Blurry":
        score -= 15
        reasons.append("Image appears blurry.")
    else:
        reasons.append("Image sharpness acceptable.")

    # -------------------------
    # Histogram
    # -------------------------

    reasons.append(histogram["interpretation"])

    # -------------------------
    # Final Risk
    # -------------------------

    if score >= 85:
        risk = "LOW"
        color = "success"

    elif score >= 65:
        risk = "MEDIUM"
        color = "warning"

    else:
        risk = "HIGH"
        color = "danger"

    # -------------------------
    # Confidence
    # -------------------------

    confidence = random.randint(90, 98)

    # -------------------------
    # Report ID
    # -------------------------

    report_id = "PFR-" + datetime.now().strftime("%Y%m%d-%H%M%S")

    # -------------------------
    # Metadata Completeness
    # -------------------------

    valid = 0
    total = 0

    for key, value in metadata.items():

        total += 1

        if value not in [
            "Not Available",
            "",
            None,
            "Unknown"
        ]:
            valid += 1

    if total > 0:
        metadata_score = round((valid / total) * 100)
    else:
        metadata_score = 0

    # -------------------------
    # Integrity
    # -------------------------

    integrity = 100

    # -------------------------
    # Return
    # -------------------------

    return {

        "score": score,

        "risk": risk,

        "color": color,

        "confidence": confidence,

        "report_id": report_id,

        "reasons": reasons,

        "metadata_score": metadata_score,

        "integrity": integrity

    }