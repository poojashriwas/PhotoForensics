from PIL import Image, ImageChops, ImageEnhance, ImageStat
import cv2
import numpy as np
import os


def generate_ela(image_path):

    filename = os.path.basename(image_path)

    temp_image = "static/ela/temp.jpg"

    ela_output = f"static/ela/ela_{filename}"

    highlight_output = f"static/ela/highlight_{filename}"

    image = Image.open(image_path).convert("RGB")

    image.save(temp_image, "JPEG", quality=90)

    temp = Image.open(temp_image)

    diff = ImageChops.difference(image, temp)

    extrema = diff.getextrema()

    max_diff = max(ex[1] for ex in extrema)

    if max_diff == 0:
        max_diff = 1

    scale = 255.0 / max_diff

    diff = ImageEnhance.Brightness(diff).enhance(scale)

    diff.save(ela_output)

    # -------------------------
    # OpenCV Analysis
    # -------------------------

    ela_cv = cv2.imread(ela_output)

    gray = cv2.cvtColor(ela_cv, cv2.COLOR_BGR2GRAY)

    # Blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive Threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        21,
        8
    )

    # Remove Noise
    kernel = np.ones((3, 3), np.uint8)

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1
    )

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    region_count = 0
    largest_area = 0

    for contour in contours:

        area = cv2.contourArea(contour)

        # Ignore very small regions
        if area < 350:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        # Ignore tiny boxes
        if w < 20 or h < 20:
            continue

        cv2.rectangle(
            ela_cv,
            (x, y),
            (x + w, y + h),
            (0, 0, 255),
            2
        )

        region_count += 1

        if area > largest_area:
            largest_area = area

    cv2.imwrite(highlight_output, ela_cv)

    # -------------------------
    # ELA Score
    # -------------------------

    stat = ImageStat.Stat(diff)

    ela_score = sum(stat.mean) / len(stat.mean)

    # -------------------------
    # Better Risk Classification
    # -------------------------

    if ela_score < 15 and region_count < 5:
        risk = "Low"
        color = "success"

    elif ela_score < 35 or region_count < 15:
        risk = "Medium"
        color = "warning"

    else:
        risk = "High"
        color = "danger"

    return {

        "ela_image": ela_output,

        "highlight_image": highlight_output,

        "ela_score": round(ela_score, 2),

        "risk": risk,

        "color": color,

        "regions": region_count,

        "largest_region": int(largest_area)

    }