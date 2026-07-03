from flask import Flask, render_template, request
import os

from modules.hashing import calculate_hashes
from modules.fileinfo import get_file_info
from modules.metadata import extract_metadata
from modules.gps import extract_gps

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    image = request.files["image"]

    if image.filename == "":
        return "No image selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)

    image.save(filepath)

    # File Information
    file_info = get_file_info(filepath)

    # EXIF Metadata
    metadata = extract_metadata(filepath)

    # Hash Information
    hash_info = calculate_hashes(filepath)

    # GPS Information
    gps_info = extract_gps(filepath)

    # Google Maps Link
    google_maps_url = None

    if gps_info.get("Status") == "GPS Coordinates Found":

        latitude = gps_info["Latitude"]
        longitude = gps_info["Longitude"]

        google_maps_url = (
            f"https://www.google.com/maps?q={latitude},{longitude}"
        )

    return render_template(
        "result.html",
        filename=image.filename,
        file_info=file_info,
        metadata=metadata,
        hash_info=hash_info,
        gps_info=gps_info,
        google_maps_url=google_maps_url
    )


if __name__ == "__main__":
    app.run(debug=True)