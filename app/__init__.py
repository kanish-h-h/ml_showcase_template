"""
Application factory - creates Flask app instance
"""

from flask import Flask, render_template
from config import Config
from datetime import datetime


def create_app(config_class=Config):
    """
    Application factory function
    Usage: app = create_app()
    """
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder="templates",
        static_folder="static",
    )

    # Load configuration
    app.config.from_object(config_class)

    # Register routes
    with app.app_context():
        from . import routes

        routes.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register template helpers
    register_template_helpers(app)

    return app


def register_error_handlers(app):
    """Register custom error pages"""

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500


def register_template_helpers(app):
    """Register custom Jinja2 filters and context processors"""

    @app.context_processor
    def utility_processor():
        """Add utility functions to all templates"""
        return {
            "app_name": app.config.get("APP_NAME", "ML Showcase"),
            "app_version": app.config.get("APP_VERSION", "1.0.0"),
            "current_year": datetime.now().year,  # ✅ Added current year
        }
