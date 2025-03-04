import logging
import sys

def setup_logging():
    # Configure structured logging in JSON format.
    formatter = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    # Ensure we don't add duplicate handlers
    if not root.handlers:
        root.addHandler(handler)
