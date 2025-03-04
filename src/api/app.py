from flask import Flask
from src.config import Config
from src.api import routes, middleware

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register the API blueprint and middleware
    app.register_blueprint(routes.api_bp)
    middleware.log_request_middleware(app)
    
    return app

# Expose the app instance for Gunicorn
app = create_app()
