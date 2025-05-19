FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Create startup script
COPY <<EOF /app/start.sh
#!/bin/bash
python manage.py migrate
gunicorn news.wsgi:application --bind 0.0.0.0:\$PORT --workers 2 --threads 2
EOF

RUN chmod +x /app/start.sh

# Expose port
EXPOSE $PORT

# Run the application
CMD ["/app/start.sh"] 