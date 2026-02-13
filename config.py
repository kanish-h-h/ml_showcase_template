"""
Configuration settings for ML Showcase Flask app
"""

import os
from datetime import timedelta
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent


class Config:
    """Base Configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production-please"
    FLASK_APP = os.environ.get("FLASK_APP", "run.py")

    # Session settings
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

    # Static files
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Upload settings (for future model uploads)
    MAX_CONTENT_LENGHT = 16 * 1024 * 1024  # 16MB max file size

    # Application settings
    APP_NAME = "ML Showcase"
    APP_VERSION = "0.0.1"

    # Model settings
    MODEL_DIR = BASE_DIR / "app" / "models"

    # CORS settings (for API)
    CORS_HEADERS = "Content-Type"


class DevelopmentConfig(Config):
    """Development Configuration"""

    DEBUG = True
    ENV = "development"
    TESTING = False

    # Enable debug toolbar (install flask-debugtoolbar to use)
    DEBUG_TB_ENABLED = True

    # Verbose Logging
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production Configuration"""

    DEBUG = True
    ENV = "production"
    TESTING = False

    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Disable debug toolbar
    DEBUG_TB_ENABLED = False

    # Quiet Logging
    LOG_LEVEL = "WARNING"


class TestingConfig(Config):
    """Testing Configuration"""

    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False


# Configuration Selector
config = {
    "development": DevelopmentConfig(),
    "production": ProductionConfig(),
    "testing": TestingConfig(),
    "default": DevelopmentConfig(),
}


def get_config():
    """Get Configuration based on environment"""
    config_name = os.getenv("FLASK_ENV", "development")
    return config.get(config_name, config["default"])
