import queue
from datetime import datetime

import jinja_partials
from flask import Flask, Response, render_template, request

from .models import Court, MessengerQueue

ALLOWED_ATTRIBUTES = {"booked", "available", "booked2h"}
updated_queue = MessengerQueue()


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
        request_addr = request.environ.get("REMOTE_ADDR")
        court = courts[court_name]
        updated_queue.update_listeners(
            datetime.now().replace(microsecond=0), request_addr,
        )
        court.update_time(datetime.now().replace(microsecond=0))
        if context in ALLOWED_ATTRIBUTES and court:
            setattr(court, context, not getattr(court, context))
        return render_template(
            "partials/court_update.html", context=context, court=court,
        )

    @app.route("/get_part/<context>/<court_name>")
    def get_part(context, court_name):
        return render_template("partials/court.html", context=context, court=court_name)

    @app.route("/get_all_courts")
    def get_all_courts():
        return render_template("partials/all_courts.html", courts=courts)

    @app.route("/events")
    def event():
        request_addr = request.environ.get("REMOTE_ADDR")

        def stream():
            stream_queue = updated_queue.new_listener(request_addr)
            while True:
                try:
                    queue_data = stream_queue.get(timeout=45)
                except queue.Empty:
                    msg_data = "data: keepalive\n\n"
                    yield msg_data
                if request_addr != queue_data["addr"]:
                    msg_data = f"event: update\ndata: <h4>Updated: {queue_data['msg']}</h4>\n\n"
                    yield msg_data

        return Response(stream(), mimetype="text/event-stream")

    return app
