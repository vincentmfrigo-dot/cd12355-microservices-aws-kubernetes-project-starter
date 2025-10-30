# Start with a Python base image (use the slim version for smaller image size)
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies
RUN apt-get update -y && \
    apt-get install -y libpq-dev && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set the PYTHONPATH to the current working directory
ENV PYTHONPATH=/app

# List the contents of /app directory to verify files are copied correctly (for debugging)
RUN ls -la /app

# Set environment variables (if needed)
ENV DB_HOST=host.docker.internal
ENV DB_PORT=5433
ENV DB_USERNAME=myuser
ENV DB_PASSWORD=vincentf12
ENV DB_NAME=mydatabase

# Expose the port the app runs on
EXPOSE 5153

# Command to run the application
CMD ["python", "app.py"]