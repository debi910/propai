# Use backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./

# Copy data pipeline
COPY data-pipeline /app/data-pipeline
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Expose port
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
