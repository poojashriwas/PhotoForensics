from flask import Flask, render_template, request
import os
import time

from modules.hashing import calculate_hashes
from modules.fileinfo import get_file_info
from modules.metadata import extract_metadata
from modules.gps import extract_gps
from modules.ela import generate_ela
from modules.quality import analyze_quality
from modules.histogram import generate_histogram
from modules.summary import generate_summary
from modules.noise import analyze_noise
from modules.ai_summary import generate_ai_summary
from modules.pdf_report import generate_pdf_report

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():  

    start_time = time.time()

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
    #ELA check
    # ELA Analysis
    ela_result = generate_ela(filepath)
     
     #Quality Info
    quality_info = analyze_quality(filepath)
     
     #histogram
    histogram_info = generate_histogram(filepath)

    noise_info = analyze_noise(filepath)

    #Summary
    summary = generate_summary(
    metadata,
    gps_info,
    ela_result,
    quality_info,
    histogram_info
)
    pdf_report = generate_pdf_report(

    summary,

    image_path,

    file_info,

    metadata,

    gps_info,

    hash_info,

    ela_result,

    quality_info,

    histogram_info,

    noise_info,

    ai_summary

)
    
    ai_summary = generate_ai_summary(
    metadata,
    gps_info,
    ela_result,
    quality_info,
    histogram_info,
    noise_info,
    summary
)
    
    processing_time = round(time.time() - start_time, 2)

    
    return render_template(
    "result.html",
    filename=image.filename,
    file_info=file_info,
    metadata=metadata,
    hash_info=hash_info,
    gps_info=gps_info,
    google_maps_url=google_maps_url,
    ela_result=ela_result,
    quality_info=quality_info,
   histogram_info=histogram_info,
   noise_info=noise_info,
   summary=summary,
   ai_summary=ai_summary,
   pdf_report=pdf_report,
   processing_time=processing_time
)


if __name__ == "__main__":
    app.run(debug=True)