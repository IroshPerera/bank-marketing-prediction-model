# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy model files and application code
COPY model/ model/
COPY . .

# Expose the Flask port
EXPOSE 80

# Run the Flask app
ENTRYPOINT ["python3", "app.py"]
