# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependencies first for caching layers
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for generated files if it doesn't exist
# (Though your app saves to root or specific path, ensuring permissions is good)
RUN chmod -R 777 /app

# Access port 10000 or $PORT environment variable
ENV PORT=10000

# Expose the port (informative)
EXPOSE $PORT

# Run Gunicorn
# -w 4: 4 worker processes for concurrency
# -b 0.0.0.0:$PORT: Bind to all interfaces on the port provided by environment
CMD gunicorn -w 4 -b 0.0.0.0:$PORT server:app
