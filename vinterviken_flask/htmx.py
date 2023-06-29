from flask import Flask, render_template
from .db import create_db
from .models import db, Court

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    create_db(app)

    #db.init_app(app)
    #with app.app_context():
    #    db.create_all()
    #    courts = [Court() for _ in range(3)]
    #    db.session.add_all(courts)
    #    db.session.commit()

    @app.route('/')
    def index():
        courts = db.session.execute(db.select(Court).order_by(Court.id)).scalars().all()
        print(courts[1].booked)
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