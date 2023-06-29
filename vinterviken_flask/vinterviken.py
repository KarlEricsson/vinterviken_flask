import jinja_partials
from flask import Flask, render_template
from .db import create_db
from .models import db, Court

def create_app():
    app = Flask(__name__)
    jinja_partials.register_extensions(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    create_db(app)

    @app.route('/')
    def index():
        courts = db.session.execute(db.select(Court).order_by(Court.id)).scalars().all()
        return render_template('index.html', courts=courts)

    @app.route('/toggle_availability/<int:court_id>', methods=['POST'])
    def toggle_availability(court_id):
        court = Court.query.get(court_id)
        if court:
            court.available = not court.available
            db.session.commit()
        return render_template('partials/colordiv.html', court=court)

    @app.route('/toggle_booking/<int:court_id>', methods=['POST'])
    def toggle_booking(court_id):
        court = Court.query.get(court_id)
        if court:
            court.booked = not court.booked
            db.session.commit()
        return render_template('partials/colordivnext.html', court=court)

    return app