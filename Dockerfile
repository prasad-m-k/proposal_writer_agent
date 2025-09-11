# Use the official Python 3.13 slim-bookworm image as the base image
FROM python:3.13-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if any are needed for Flask/Gunicorn or your app
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/* # Clean up apt cache to keep image size small

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies including Gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that your Flask app (via Gunicorn) will run on
EXPOSE 5000

# Define the command to run your Flask application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
