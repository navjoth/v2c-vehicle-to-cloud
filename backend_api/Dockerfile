# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]
