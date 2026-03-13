"""Quick test to verify admin dashboard route works."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite:///intlq.db"

from app import create_app

app = create_app()
client = app.test_client()

# Login as admin
r = client.post("/login", data={"username": "admin1", "password": "admin123"}, follow_redirects=False)
print(f"Login: status={r.status_code}, redirect_to={r.headers.get('Location')}")

# Access admin page
r2 = client.get("/admin")
print(f"Admin page: status={r2.status_code}")
print(f"Has 'Admin Dashboard': {b'Admin Dashboard' in r2.data}")
print(f"Has stat-users: {b'stat-users' in r2.data}")
print(f"Has admin1 in data: {b'admin1' in r2.data}")
print(f"Has testuser in data: {b'testuser' in r2.data}")

# Test non-admin access
r3 = client.get("/logout", follow_redirects=True)
r4 = client.post("/login", data={"username": "testuser", "password": "test123"}, follow_redirects=False)
print(f"\nNon-admin login: status={r4.status_code}")
r5 = client.get("/admin")
print(f"Non-admin admin page: status={r5.status_code}")
print(f"Has 'Access denied': {b'Access denied' in r5.data}")

print("\nAll checks passed!" if r2.status_code == 200 and r5.status_code == 403 else "\nSome checks failed!")
