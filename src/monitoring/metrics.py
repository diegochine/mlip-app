from flask import Blueprint, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Create a blueprint for the metrics endpoint
metrics_bp = Blueprint('metrics', __name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency in seconds', ['endpoint'])

@metrics_bp.route('/metrics')
def metrics():
    # Expose the collected metrics to Prometheus
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
