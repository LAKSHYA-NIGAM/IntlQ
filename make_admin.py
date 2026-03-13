"""
Admin Promotion Script
Usage: python make_admin.py <username>

Promotes a user to admin status so they can access the admin dashboard.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from database.crud import get_user_by_username, make_admin


def main():
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py <username>")
        print("Example: python make_admin.py lakshya")
        sys.exit(1)

    username = sys.argv[1]
    app = create_app()

    with app.app_context():
        user = get_user_by_username(username)
        if not user:
            print(f"❌ User '{username}' not found.")
            sys.exit(1)

        if user.is_admin:
            print(f"ℹ️  User '{username}' is already an admin.")
            sys.exit(0)

        make_admin(user.id)
        print(f"✅ User '{username}' has been promoted to admin!")
        print(f"   They can now access the dashboard at /admin")


if __name__ == "__main__":
    main()
