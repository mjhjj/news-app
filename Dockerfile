FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000
ENV DJANGO_SETTINGS_MODULE=news.settings
ENV PYTHONPATH=/app
ENV DJANGO_LOG_LEVEL=INFO

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and necessary directories
RUN useradd -m appuser && \
    mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R appuser:appuser /app

# Install Python dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser . .

# Set proper permissions
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app && \
    chmod -R 777 /app/logs

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Checking database connection..."\n\
python manage.py check --database default\n\
echo "Running migrations..."\n\
python manage.py showmigrations\n\
python manage.py migrate --noinput --verbosity 3\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput\n\
echo "Starting Gunicorn..."\n\
gunicorn news.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --log-level info --access-logfile - --error-logfile -' > /app/start.sh && \
    chmod +x /app/start.sh && \
    chown appuser:appuser /app/start.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE $PORT

# Run the application
CMD ["/app/start.sh"] 