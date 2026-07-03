from flask import Flask, render_template, request
import os

# Create Flask app
app = Flask(__name__)

# Upload folder configuration
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home page

@app.route("/")
def home():
    return render_template("index.html")


# Upload route
@app.route("/upload", methods=["POST"])
def upload():

    image = request.files["image"]

    if image.filename == "":
        return "No image selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)

    image.save(filepath)

    return render_template(
        "result.html",
        filename=image.filename
    )


    image = request.files["image"]

    if image.filename == "":
        return "No image selected."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)

    image.save(filepath)

    return render_template(
        "result.html",
        filename=image.filename
    )


# Run the application
if __name__ == "__main__":
    app.run(debug=True)