# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

# Use a stable Python version
ARG PYTHON_VERSION=3.10-slim
FROM python:${PYTHON_VERSION} as base

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Firefox and geckodriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    firefox-esr \
    wget \
    && wget -q https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.33.0-linux64.tar.gz -C /usr/local/bin \
    && rm geckodriver-v0.33.0-linux64.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install sqlite3
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for geckodriver
ENV PATH="/usr/local/bin:$PATH"

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-privileged user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create the directory for the database file and set permissions
RUN mkdir -p /app/db && chown -R appuser:appuser /app/db

# Create the directory for the log file and set permissions
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs && chmod -R u+rw /app/logs

# Set ownership and permissions for the /app folder and its subfolders
RUN chown -R appuser:appuser /app && chmod -R u+rw /app

# Set an environment variable for the database path
ENV DB_NAME=/app/db/database.sqlite

# Set an environment variable for the log file path
ENV LOG_FILE=/app/logs/myapp.log

# Expose the port the application will run on (if applicable)
EXPOSE 8000

# Switch to the non-privileged user to run the application
USER root

# Set the default command to run the application and keep the container running
CMD ["sh", "-c", "python main.py --scrape --all || echo 'Script failed, keeping container alive' && tail -f /dev/null"]
