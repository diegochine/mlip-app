from flask import request

def log_request_middleware(app):
    @app.before_request
    def log_request():
        app.logger.info(f"Incoming request: {request.method} {request.path}")
