from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    admin = User(username='admin', is_admin=True)
    admin.set_password('admin_password')
    db.session.add(admin)
    db.session.commit()
    print("Database initialized and admin user created.")
