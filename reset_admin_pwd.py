from app import create_app
from database.crud import get_all_users
from database.db import db
import sys

app = create_app()
with app.app_context():
    users = get_all_users()
    admins = [u for u in users if u.is_admin]
    if not admins:
        print("No admin users found.")
        sys.exit(1)
    
    for admin in admins:
        admin.set_password("admin123")
        db.session.commit()
        print(f"Password for admin '{admin.username}' reset to: admin123")
