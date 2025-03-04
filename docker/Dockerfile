# Use the official lightweight Python image.
FROM python:3.9-slim

# Prevent Python from writing pyc files to disc and enables stdout/stderr logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container.
WORKDIR /app

# Install dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files into the container.
COPY . /app/

# Expose the port the app runs on.
EXPOSE 5000

# Run the application using Gunicorn.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.api.app:app"]
