# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies for PostgreSQL and building Python packages
RUN apt update -y && \
    apt install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file first for caching purposes
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that Flask app runs on
EXPOSE 5153

# Set environment variables (optional defaults)
ENV DB_USERNAME=myuser
ENV DB_PASSWORD=vincentf12
ENV DB_HOST=127.0.0.1
ENV DB_PORT=5433
ENV DB_NAME=mydatabase

# Command to run the app
CMD ["python", "app.py"]
