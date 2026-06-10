# Use official Python lightweight image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8080

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and default memory mount path
COPY main.py .

# Expose the application port
EXPOSE 8080

# Command to run uvicorn server
CMD ["python", "main.py"]
