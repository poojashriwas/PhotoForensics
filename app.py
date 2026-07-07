from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login import current_user
from datetime import datetime
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
from config import Config
from models import db, User, Investigation
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
print("=" * 50)
print("ROOT PATH:", app.root_path)
print("TEMPLATE FOLDER:", app.template_folder)
print("=" * 50)
bcrypt = Bcrypt(app)

app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

import os

with app.app_context():
    db.create_all()

    print("=" * 50)
    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Root DB:", os.path.abspath("database.db"))
    print("Instance DB:", os.path.join(app.instance_path, "database.db"))
    print("=" * 50)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)




@app.route("/")
def home():
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():

    investigations = Investigation.query.filter_by(
        user_id=current_user.id
    ).all()

    total_cases = len(investigations)

    high_risk = len([
        i for i in investigations
        if i.risk == "HIGH"
    ])

    avg_score = 0

    if total_cases > 0:

        avg_score = round(

            sum(i.score for i in investigations)

            / total_cases

        )

    from datetime import date

    today_cases = len([
        i for i in investigations
        if i.created_at.date() == date.today()
    ])

    recent_cases = Investigation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Investigation.created_at.desc()
    ).limit(5).all()

    low_cases = len([
    i for i in investigations
    if i.risk == "LOW"
])

    medium_cases = len([
    i for i in investigations
    if i.risk == "MEDIUM"
])

    high_cases = len([
    i for i in investigations
    if i.risk == "HIGH"
])

    return render_template(

    "dashboard.html",

    total_cases=total_cases,
    high_risk=high_risk,
    avg_score=avg_score,
    today_cases=today_cases,
    recent_cases=recent_cases,

    low_cases=low_cases,
    medium_cases=medium_cases,
    high_cases=high_cases

)

@app.route("/new")
@login_required
def new():

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered."

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        print("Registered User:", new_user.id, new_user.email)

        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()
    print("Searching:", email)
    print("Found:", user.email if user else "No User Found")

    if user and bcrypt.check_password_hash(user.password, password):

        login_user(user)

        return redirect("/dashboard")

    return "Invalid Email or Password"

@app.route("/loading")
@login_required
def loading():
    return render_template("loading.html")


@app.route("/upload", methods=["POST"])
@login_required
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
    
    ai_summary = generate_ai_summary(
    metadata,
    gps_info,
    ela_result,
    quality_info,
    histogram_info,
    noise_info,
    summary
)
    pdf_report = generate_pdf_report(

    summary,

    filepath,

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
    
    # -----------------------------
    # Save Investigation
    # -----------------------------

    case_id = "CASE-" + datetime.now().strftime("%Y%m%d%H%M%S")

    new_case = Investigation(

    case_id=case_id,

    filename=image.filename,

    risk=summary["risk"],

    score=summary["score"],

    confidence=summary["confidence"],

    report_path=pdf_report,

    created_at=datetime.now(),

    user_id=current_user.id

)

    db.session.add(new_case)
    db.session.commit()
    
   
    
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
   case_id=case_id,
   processing_time=processing_time
)
@app.route("/history")
@login_required
def history():

    investigations = Investigation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Investigation.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        investigations=investigations
    )

@app.route("/profile")
@login_required
def profile():

    investigations = Investigation.query.filter_by(
        user_id=current_user.id
    ).all()

    total_cases = len(investigations)

    avg_score = 0

    if total_cases:

        avg_score = round(
            sum(i.score for i in investigations)/total_cases
        )

    high_risk = len(
        [i for i in investigations if i.risk=="HIGH"]
    )

    return render_template(

        "profile.html",

        total_cases=total_cases,

        avg_score=avg_score,

        high_risk=high_risk

    )

@app.route("/reports")
@login_required
def reports():

    reports = Investigation.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Investigation.created_at.desc()
    ).all()

    # Total Reports
    total_reports = len(reports)

    # Downloaded Reports
    downloaded = len([
    r for r in reports
    if r.report_path
])

    # Average Score
    if reports:
        avg_score = round(
            sum(r.score for r in reports) / len(reports)
        )
    else:
        avg_score = 0

    # High Risk Reports
    high_risk = len([
        r for r in reports
        if r.risk == "HIGH"
    ])

    return render_template(

        "reports.html",

        reports=reports,

        total_reports=total_reports,

        downloaded=downloaded,

        avg_score=avg_score,

        high_risk=high_risk

    )

@app.route("/search")
@login_required
def search():

    query = request.args.get("q", "")

    reports = Investigation.query.filter(
        Investigation.filename.contains(query)
    ).all()

    return render_template(
        "dashboard.html",
        reports=reports
    )

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)