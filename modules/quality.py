import cv2
import numpy as np


def analyze_quality(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resolution
    height, width = gray.shape

    resolution = f"{width} × {height}"

    # Blur Detection (Laplacian Variance)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur_score < 100:
        blur = "Blurry"

    elif blur_score < 300:
        blur = "Moderate"

    else:
        blur = "Sharp"

    # Brightness
    brightness = np.mean(gray)

    if brightness < 70:
        brightness_status = "Dark"

    elif brightness < 180:
        brightness_status = "Normal"

    else:
        brightness_status = "Bright"

    # Contrast
    contrast = np.std(gray)

    if contrast < 30:
        contrast_status = "Low"

    elif contrast < 70:
        contrast_status = "Normal"

    else:
        contrast_status = "High"

    return {

        "resolution": resolution,

        "blur_score": round(blur_score, 2),

        "blur": blur,

        "brightness": round(brightness, 2),

        "brightness_status": brightness_status,

        "contrast": round(contrast, 2),

        "contrast_status": contrast_status

    }