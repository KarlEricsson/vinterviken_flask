import queue
from datetime import datetime

import jinja_partials
from flask import Flask, Response, render_template

from .db import create_db
from .models import Court, db

ALLOWED_ATTRIBUTES = {"booked", "available", "booked2h"}
updated_time = "Not updated since server restart."
updated_queue = queue.Queue(maxsize=1)


def create_app():
    app = Flask(__name__)
    jinja_partials.register_extensions(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    create_db(app)

    @app.route("/")
    def index():
        courts = db.session.execute(db.select(Court).order_by(Court.id)).scalars().all()
        return render_template("index.html", courts=courts, updated_time=updated_time)

    @app.route("/toggle_status/<context>/<int:court_id>", methods=["POST"])
    def toggle_status(context: str, court_id):
        global updated_time
        updated_queue.put(datetime.now().replace(microsecond=0))
        updated_time = datetime.now().replace(microsecond=0)
        court = db.session.get(Court, court_id)
        if context in ALLOWED_ATTRIBUTES and court:
            setattr(court, context, not getattr(court, context))
            db.session.commit()
        return render_template("partials/court.html", context=context, court=court)

    @app.route("/events")
    def event():
        def stream():
            while True:
                msg = f"data: <h4>Updated: {updated_queue.get()}</h4>\n\n"
                yield msg

        return Response(stream(), mimetype="text/event-stream")

    return app
