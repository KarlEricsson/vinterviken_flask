import queue
from datetime import datetime

import jinja_partials
from flask import Flask, Response, render_template

from .models import Court

ALLOWED_ATTRIBUTES = {"booked", "available", "booked2h"}
updated_queue = queue.Queue(maxsize=1)


def create_app():
    app = Flask(__name__)
    jinja_partials.register_extensions(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    court_names = ("Grusbanan", "Mittbanan", "Skogsbanan")
    courts = {name: Court(name) for name in court_names}

    @app.route("/")
    def index():
        return render_template("index.html", courts=courts)

    @app.route("/toggle_status/<context>/<court_name>", methods=["POST"])
    def toggle_status(context: str, court_name):
        updated_queue.put(datetime.now().replace(microsecond=0))
        court = courts[court_name]
        court.update_time(datetime.now().replace(microsecond=0))
        if context in ALLOWED_ATTRIBUTES and court:
            setattr(court, context, not getattr(court, context))
        return render_template("partials/court.html", context=context, court=court)

    @app.route("/events")
    def event():
        def stream():
            while True:
                msg = f"data: <h4>Updated: {updated_queue.get()}</h4>\n\n"
                yield msg

        return Response(stream(), mimetype="text/event-stream")

    return app
