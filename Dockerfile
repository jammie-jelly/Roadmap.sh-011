# Use an official Python slim runtime as base
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the code
COPY app /app/app
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the backend API server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

