from .models import Court, db


def create_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        courts = [Court() for _ in range(3)]
        db.session.add_all(courts)
        db.session.commit()
