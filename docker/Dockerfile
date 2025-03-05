FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and configuration
COPY ../src ./src
COPY ../.env .

# Expose port 3000 for the Flask app
EXPOSE 3000

# Start the Flask application using Gunicorn with 4 workers
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "src.api.app:app", "--workers", "4"]
