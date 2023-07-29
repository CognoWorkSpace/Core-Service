# Use the official Python base image with Ubuntu 20.04
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app

# Update and install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy all the files from the current directory to the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=manage.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
# Start the Flask application
CMD ["flask", "run"]