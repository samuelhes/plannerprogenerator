FROM python:3.10-slim

# 1. Set environment variables to prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=server.py

# 2. Set work directory
WORKDIR /app

# 3. Create a non-root user
RUN adduser --disabled-password --gecos '' appuser

# 4. Install dependencies
# Copy only requirements first to cache layer
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# 5. Copy project code
COPY . /app/

# 6. Change ownership to non-root user
RUN chown -R appuser:appuser /app

# 7. Switch to non-root user
USER appuser

# 8. Expose port (Cloud Run sets PORT env var, we just expose 8080 as a hint)
EXPOSE 8080

# 9. Run Gunicorn
# Bind to 0.0.0.0:$PORT
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app
