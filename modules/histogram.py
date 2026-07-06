import matplotlib
matplotlib.use("Agg")
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os


def generate_histogram(image_path):

    image = cv2.imread(image_path)

    colors = ("b", "g", "r")

    plt.figure(figsize=(8,4))

    means = {}

    for color in colors:

        hist = cv2.calcHist(
            [image],
            [colors.index(color)],
            None,
            [256],
            [0,256]
        )

        plt.plot(hist, color=color)

        means[color] = np.mean(image[:, :, colors.index(color)])

        plt.xlim([0,256])

        plt.title("RGB Color Histogram", fontsize=14, fontweight="bold")

        plt.xlabel("Pixel Intensity", fontsize=11)

        plt.ylabel("Frequency", fontsize=11)

        plt.grid(True, alpha=0.3)

        plt.legend(
    ["Blue Channel", "Green Channel", "Red Channel"],
    loc="upper left"
)

    plt.tight_layout()

    filename = os.path.splitext(os.path.basename(image_path))[0]

    output = f"static/histograms/histogram_{filename}.png"

    os.makedirs("static/histograms", exist_ok=True)

    plt.savefig(output, bbox_inches="tight")

    plt.close()

    # ------------------------
    # Histogram Analysis
    # ------------------------

    dominant = max(means, key=means.get)

    if dominant == "r":
        dominant_color = "Red"

    elif dominant == "g":
        dominant_color = "Green"

    else:
        dominant_color = "Blue"

    brightness = np.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

    if brightness < 80:
        brightness_level = "Dark"

    elif brightness < 180:
        brightness_level = "Normal"

    else:
        brightness_level = "Bright"

    contrast = np.std(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

    if contrast < 30:
        contrast_level = "Low"

    elif contrast < 70:
        contrast_level = "Normal"

    else:
        contrast_level = "High"

    # ------------------------
# Smart Forensic Interpretation
# ------------------------

    if brightness_level == "Bright" and contrast_level == "High":

     interpretation = (
        "Image appears highly exposed with strong contrast. "
        "Possible brightness enhancement or harsh lighting."
    )

    elif brightness_level == "Dark":

     interpretation = (
        "Image appears underexposed. Dark regions may hide visual details."
    )

    elif dominant_color == "Red":

     interpretation = (
        "Red channel dominates the image. "
        "This may result from lighting conditions or color enhancement."
    )

    elif dominant_color == "Green":

     interpretation = (
        "Green channel dominates the image. "
        "Typical for outdoor scenes or green illumination."
    )

    elif dominant_color == "Blue":

     interpretation = (
        "Blue channel dominates the image. "
        "May indicate sky, water or cool color temperature."
    )

    elif contrast_level == "High":

     interpretation = (
        "High contrast detected. Image contains strong intensity variations."
    )

    else:

     interpretation = (
        "Histogram distribution appears balanced without obvious abnormalities."
    )
     
     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

     mean_intensity = round(np.mean(gray), 2)

     dynamic_range = int(gray.max() - gray.min())

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    mean_intensity = round(np.mean(gray), 2)

    dynamic_range = int(gray.max() - gray.min())


    if dynamic_range > 200:

     dynamic_text = "Wide"

    elif dynamic_range > 120:

     dynamic_text = "Medium"

    else:

     dynamic_text = "Narrow"

    return {

    "histogram_image": output,

    "dominant_color": dominant_color,

    "brightness_level": brightness_level,

    "contrast_level": contrast_level,

    "mean_intensity": mean_intensity,

    "dynamic_range": dynamic_text,

    "interpretation": interpretation

}