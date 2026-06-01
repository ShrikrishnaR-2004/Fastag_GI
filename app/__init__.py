from flask import Flask, redirect, url_for
from config import config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import models  # noqa: F401

    # Automatically create database tables if they don't exist yet
    with app.app_context():
        db.create_all()

    # ── Blueprints ──────────────────────────────────────────────────
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.dashboard import bp as dash_bp
    app.register_blueprint(dash_bp, url_prefix='/app')

    # ── Root / legacy redirects ─────────────────────────────────────
    @app.route('/')
    def index():
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('dash.overview'))
        return redirect(url_for('auth.login'))

    # Keep /dashboard working as a redirect so old links don't break
    @app.route('/dashboard')
    def dashboard():
        return redirect(url_for('dash.overview'))

    @app.after_request
    def add_header(response):
        """Prevent browser caching to fix the 'back button after logout' issue."""
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"]        = "no-cache"
        response.headers["Expires"]       = "0"
        return response

    return app
