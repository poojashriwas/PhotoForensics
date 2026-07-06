from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    investigations = db.relationship(
        "Investigation",
        backref="user",
        lazy=True
    )


class Investigation(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    case_id = db.Column(
        db.String(30),
        unique=True
    )

    filename = db.Column(
        db.String(255)
    )

    risk = db.Column(
        db.String(20)
    )

    score = db.Column(
        db.Integer
    )

    confidence = db.Column(
        db.Integer
    )

    report_path = db.Column(
        db.String(300)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )