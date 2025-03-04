from flask import Flask
from src.config import Config
from src.api import routes, middleware
from src.monitoring import logging_config
from src.monitoring import metrics

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup structured logging
    logging_config.setup_logging()
    
    # Register API and monitoring blueprints
    app.register_blueprint(routes.api_bp)
    app.register_blueprint(metrics.metrics_bp)  # Exposes the /metrics endpoint
    
    # Setup middleware for logging and metrics
    middleware.log_request_middleware(app)
    
    return app

# Expose the app instance for Gunicorn
app = create_app()
