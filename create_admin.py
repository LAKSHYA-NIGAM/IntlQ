from app import create_app
from database.db import db
from database.crud import create_user, make_admin, get_user_by_username
import os

app = create_app()

with app.app_context():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///intlq.db"
    db.create_all()
    
    # Create the user the user wants
    username = "admin1"
    password = "admin123"
    
    user = get_user_by_username(username)
    if not user:
        user = create_user(username, f"{username}@example.com", password)
        make_admin(user.id)
        print(f"Created user: {username} / {password} with admin privileges.")
    else:
        # Update user to make sure password is correct (we can't easily update password in crud without a function, let's just recreate or leave it)
        user.set_password(password)
        make_admin(user.id)
        db.session.commit()
        print(f"Updated user: {username} with admin privileges and reset password.")

    # Also make sure there is a default candidate if needed
