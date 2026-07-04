import cv2
import numpy as np
import os


def analyze_noise(image_path):

    filename = os.path.splitext(os.path.basename(image_path))[0]

    output = f"static/noise/noise_{filename}.png"

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Estimate noise using Laplacian
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    noise_level = laplacian.var()

    normalized = cv2.convertScaleAbs(laplacian)

    cv2.imwrite(output, normalized)

    if noise_level < 100:

        risk = "Low"

        color = "success"

    elif noise_level < 500:

        risk = "Medium"

        color = "warning"

    else:

        risk = "High"

        color = "danger"

    return {

        "noise_image": output,

        "noise_score": round(noise_level,2),

        "risk": risk,

        "color": color

    }