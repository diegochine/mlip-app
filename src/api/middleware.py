import time
from flask import request, g
import logging
from src.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY

def log_request_middleware(app):
    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def log_and_record_metrics(response):
        latency = time.time() - g.start_time if hasattr(g, 'start_time') else 0
        # Record latency and request count for metrics collection
        REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path, http_status=response.status_code).inc()
        
        # Log request details in structured format
        app.logger.info(f"{request.method} {request.path} completed in {latency:.4f}s with status {response.status_code}")
        return response
