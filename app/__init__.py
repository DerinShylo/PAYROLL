from flask import Flask
from config import Config
from models import db, ensure_admin_exists
from routes import routes, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(routes)

    # ✅ Ensure admin exists on first run
    ensure_admin_exists(app)

    return app
