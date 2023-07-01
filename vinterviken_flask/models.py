from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Court(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    available = db.Column(db.Boolean, default=True)
    booked = db.Column(db.Boolean, default=False)
    booked2h = db.Column(db.Boolean, default=False)
