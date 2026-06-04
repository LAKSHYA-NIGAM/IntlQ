from app import create_app
from database.db import db
from database.crud import create_user, make_admin, get_user_by_username
import os

app = create_app()

with app.app_context():
    # Force DB creation locally in current directory
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///intlq.db"
    db.create_all()
    user = get_user_by_username("admin")
    if not user:
        user = create_user("admin", "admin@intlq.com", "password")
        make_admin(user.id)
        print("Created admin user: admin / password")
    else:
        print("Admin user already exists.")
