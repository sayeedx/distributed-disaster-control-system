FROM python:3.10-slim

WORKDIR /app

# Copy ONLY what we need (clean + guaranteed)
COPY services/allocation_service /app/services/allocation_service
COPY services/shared /app/services/shared

RUN pip install --no-cache-dir -r /app/services/allocation_service/requirements.txt

CMD ["python", "/app/services/allocation_service/app/main.py"]