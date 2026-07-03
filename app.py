from flask import Flask, render_template, request
import os

from modules.fileinfo import get_file_info
from modules.metadata import extract_metadata

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

    # Extract File Information
    file_info = get_file_info(filepath)

    # Extract Metadata
    metadata = extract_metadata(filepath)

    return render_template(
        "result.html",
        filename=image.filename,
        file_info=file_info,
        metadata=metadata
    )


if __name__ == "__main__":
    app.run(debug=True)