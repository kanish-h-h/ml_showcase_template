"""
Application entry point
Run with: python run.py
"""

import os
import sys
from app import create_app  # db
from config import get_config

# Get configuration
config_class = get_config()

# Create Flask app
app = create_app(config_class)

# Development server runner
if __name__ == "__main__":
    # Print startup info
    print("=" * 60)
    print(f"🚀 {config_class.APP_NAME} v{config_class.APP_VERSION}")
    print(f"📍 Environment: {config_class.ENV}")
    print(f"🔧 Debug mode: {'ON' if config_class.DEBUG else 'OFF'}")
    print("📡 Server running at: http://localhost:5949")
    print("=" * 60)

    # Run development server
    app.run(
        host="0.0.0.0", port=int(os.environ.get("PORT", 5949)), debug=config_class.DEBUG
    )
