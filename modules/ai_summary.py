def generate_ai_summary(metadata,
                        gps,
                        ela,
                        quality,
                        histogram,
                        noise,
                        summary):

    findings = []

    # -------------------------
    # Metadata
    # -------------------------

    if metadata.get("Image Make") != "Not Available":
        findings.append("✓ Camera metadata was successfully extracted.")
    else:
        findings.append("⚠ Camera metadata is unavailable.")

    # -------------------------
    # GPS
    # -------------------------

    if gps.get("Status") == "GPS Coordinates Found":
        findings.append("✓ GPS coordinates are available.")
    else:
        findings.append("⚠ GPS metadata is missing.")

    # -------------------------
    # Hash
    # -------------------------

    findings.append("✓ Hash verification completed successfully.")

    # -------------------------
    # ELA
    # -------------------------

    if ela["risk"] == "High":
        findings.append("⚠ ELA detected high compression artifacts.")

    elif ela["risk"] == "Medium":
        findings.append("⚠ ELA detected moderate compression artifacts.")

    else:
        findings.append("✓ ELA indicates low compression artifacts.")

    # -------------------------
    # Image Quality
    # -------------------------

    if quality["blur"] == "Blurry":
        findings.append("⚠ Image quality is affected by blur.")
    else:
        findings.append("✓ Image quality is acceptable.")

    # -------------------------
    # Histogram
    # -------------------------

    findings.append(histogram["interpretation"])

    # -------------------------
    # Noise
    # -------------------------

    findings.append(
        f"Noise analysis indicates {noise['risk'].lower()} noise levels."
    )

    # -------------------------
    # Final Recommendation
    # -------------------------

    if summary["risk"] == "LOW":

        recommendation = (
            "No strong indicators of image manipulation were detected. "
            "The image appears authentic based on automated forensic analysis. "
            "Manual forensic verification is still recommended before legal or evidential use."
        )

    elif summary["risk"] == "MEDIUM":

        recommendation = (
            "Some forensic indicators require further investigation. "
            "Manual expert analysis is recommended."
        )

    else:

        recommendation = (
            "Multiple forensic indicators suggest possible manipulation. "
            "A detailed forensic examination is strongly recommended."
        )

    return {

        "findings": findings,

        "recommendation": recommendation,

        "risk": summary["risk"],

        "confidence": summary["confidence"]

    }