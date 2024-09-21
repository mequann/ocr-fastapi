# Use official Python runtime as a base image
FROM python:3.11-slim

# Install tesseract OCR and other dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev python3-opencv

# Set work directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
