from .htmx import app, db
from .models import Court

with app.app_context():
    db.create_all()
    courts = [Court() for _ in range(3)]
    db.session.add_all(courts)
    db.session.commit()