import os
import nltk
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

# ── Download NLTK data on first run ──────────────────────────────────────────
import tempfile
nltk_data_dir = os.path.join(tempfile.gettempdir(), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
if nltk_data_dir not in nltk.data.path:
    nltk.data.path.append(nltk_data_dir)

nltk_packages = ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]
for pkg in nltk_packages:
    try:
        nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg, download_dir=nltk_data_dir, quiet=True)


def create_app():
    """Flask application factory."""
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "frontend", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "frontend", "static"),
    )

    # ── Configuration ────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    # Render uses postgres:// but SQLAlchemy needs postgresql://
    database_url = os.getenv("DATABASE_URL", "sqlite:///intlq.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    # Vercel read-only file system fix for default SQLite database
    if os.getenv("VERCEL") == "1" and database_url == "sqlite:///intlq.db":
        import shutil
        tmp_db_path = "/tmp/intlq.db"
        if not os.path.exists(tmp_db_path) and os.path.exists("intlq.db"):
            try:
                shutil.copy2("intlq.db", tmp_db_path)
            except Exception:
                pass
        database_url = f"sqlite:///{tmp_db_path}"

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── Database ─────────────────────────────────────────────────────────────
    from database.db import db
    db.init_app(app)

    with app.app_context():
        from database import models  # noqa: F401 — registers models
        db.create_all()
        
        # Prepopulate demo admin so login sessions survive ephemeral Vercel container resets
        try:
            from database.crud import get_user_by_username, create_user, make_admin
            user = get_user_by_username("admin1")
            if not user:
                new_user = create_user("admin1", "admin1@intlq.com", "admin123")
                make_admin(new_user.id)
            else:
                user.set_password("admin123")
                make_admin(user.id)
                db.session.commit()
        except Exception:
            pass

    # ── Flask-Login ──────────────────────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.login_view = "api.login_page"
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from database.crud import get_user_by_id
        return get_user_by_id(int(user_id))
        
    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import request, jsonify, redirect, url_for
        if request.path.startswith('/api/'):
            return jsonify({"error": "Authentication required. On Vercel, your user may vanish due to ephemeral storage without Postgres! Please sign in again."}), 401
        return redirect(url_for("api.login_page", next=request.path))

    # ── Blueprints ───────────────────────────────────────────────────────────
    from api.routes import api_bp
    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    debug = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    app.run(debug=debug, port=5000)
