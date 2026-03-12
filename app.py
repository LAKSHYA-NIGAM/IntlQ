import os
import nltk
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

# ── Download NLTK data on first run ──────────────────────────────────────────
nltk_packages = ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]
for pkg in nltk_packages:
    try:
        nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)


def create_app():
    """Flask application factory."""
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "frontend", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "frontend", "static"),
    )

    # ── Configuration ────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///intlq.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ── Database ─────────────────────────────────────────────────────────────
    from database.db import db
    db.init_app(app)

    with app.app_context():
        from database import models  # noqa: F401 — registers models
        db.create_all()

    # ── Flask-Login ──────────────────────────────────────────────────────────
    login_manager = LoginManager()
    login_manager.login_view = "api.login_page"
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from database.crud import get_user_by_id
        return get_user_by_id(int(user_id))

    # ── Blueprints ───────────────────────────────────────────────────────────
    from api.routes import api_bp
    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    debug = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    app.run(debug=debug, port=5000)
