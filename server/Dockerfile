# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
# Copy requirements file first to leverage Docker cache
COPY server/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY server/ ./

# Expose the application port
EXPOSE 6767

# Set the entry point for the application
CMD ["python", "main.py"]

